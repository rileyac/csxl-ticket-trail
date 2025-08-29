"""
Defines service layer for similar tickets API.
"""

from datetime import datetime
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.office_hours.similar_tickets_ai import SimilarTicketsResponse
from backend.models.office_hours.ticket_type import TicketType
from backend.services.office_hours.similar_tickets_ai import SimilarTicketAIService
from ...database import db_session
from ...models.user import User
from ...models.academics.section_member import RosterRole
from ...models.academics.my_courses import (
    OfficeHourTicketOverview,
)
from ...models.office_hours.ticket import (
    TicketState,
    NewOfficeHoursTicket,
    OfficeHoursTicket,
)

from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours import (
    CourseSiteEntity,
    OfficeHoursEntity,
    OfficeHoursTicketEntity,
)
from ...entities.academics.section_member_entity import SectionMemberEntity
from ..exceptions import CoursePermissionException, ResourceNotFoundException
from ...entities.office_hours import user_created_tickets_table

__authors__ = ["Riley Chapman, Sarah Glenn"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


class OfficeHourSimilarTicketService:
    """
    Service that performs all of the actions for fetching similar office hour tickets.
    """

    def __init__(
        self,
        session: Session = Depends(db_session),
        ai_service: SimilarTicketAIService = Depends(),
    ):
        """
        Initializes the database session.
        """
        self._session = session
        self._ai_service = ai_service

    def find_similar_tickets(self, subject: User, id: int) -> SimilarTicketsResponse:
        """
        Builds the AI prompt and compiles all past tickets in the database to be sifted through by AI.
        Makes a call to the AI service layer andvuses the AI response
        to compile a list of actual tickets to return to the API.

        Args:
            subject (User): The user requesting the tickets.
            id (int): The ID of the ticket that is currently open.

        Returns:
            SimilarTicketsResponse: List of similar tickets.
        """
        ticket_entity = self._session.get(OfficeHoursTicketEntity, id)
        if not ticket_entity:
            raise ResourceNotFoundException(f"Ticket not found with ID: {id}")

        # Testing adding course permissions here
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == subject.id)
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == ticket_entity.office_hours_id)
        )
        user_members = self._session.scalars(user_member_query).unique().all()
        user_member = user_members[0] if len(user_members) > 0 else None

        # Ensure that the user is a TA or Instructor for the office hours session
        if not user_member or user_member.member_role not in [
            RosterRole.UTA,
            RosterRole.INSTRUCTOR,
            RosterRole.GTA,
        ]:
            raise CoursePermissionException(
                "Not allowed to view similar tickets unless you are a TA or Instructor for the course."
            )

        # prepping input for AI call
        prompt_input = {}
        if ticket_entity.type == TicketType.CONCEPTUAL_HELP:
            prompt_input = {
                "concept_help_description": ticket_entity.concept_help_description,
            }
        else:
            prompt_input = {
                "assignment_section_description": ticket_entity.assignment_section_description,
                "code_to_english_description": ticket_entity.code_to_english_description,
                "concepts_needed_description": ticket_entity.concepts_needed_description,
                "tactics_tried": ticket_entity.tactics_tried,
            }

        # Based on sqlalchemy reading part 4 (read section)
        query = select(OfficeHoursTicketEntity).where(
            OfficeHoursTicketEntity.state == TicketState.CLOSED
        )
        all_entities = self._session.scalars(query).all()
        past_tickets = [entity.to_overview_model() for entity in all_entities]

        # call AI and get similar ticket ids from AI using the similarticketAiresponse model
        ai_response = self._ai_service.ai_for_similar_tickets(
            prompt_input, past_tickets
        )
        similar_ids = ai_response.similar_ticket_ids

        if not similar_ids:
            return SimilarTicketsResponse(similar_tickets=[])

        # get tickets with ids given by AI from the database - also based on sqlalchemy reading part 4
        filtered_query = select(OfficeHoursTicketEntity).where(
            OfficeHoursTicketEntity.id.in_(similar_ids)
        )
        filtered_entities = self._session.scalars(filtered_query).all()
        filtered_ticket_overviews = [
            entity.to_overview_model() for entity in filtered_entities
        ]
        return SimilarTicketsResponse(similar_tickets=filtered_ticket_overviews)
