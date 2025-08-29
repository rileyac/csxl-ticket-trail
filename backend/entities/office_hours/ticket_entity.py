"""Definition of SQLAlchemy table-backed object mapping entity for Office Hour tickets."""

from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from backend.entities.user_entity import UserEntity
from backend.models.academics.my_courses import OfficeHourTicketOverview

# from backend.models.public_user import PublicUser

from ...models.office_hours.ticket_state import TicketState
from ...models.office_hours.ticket_type import TicketType
from ...models.office_hours.ticket import OfficeHoursTicket, NewOfficeHoursTicket
from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from .user_created_tickets_table import user_created_tickets_table


from ..entity_base import EntityBase
from typing import Self
from sqlalchemy import Enum as SQLAlchemyEnum

__authors__ = [
    "Ajay Gandecha",
    "Madelyn Andrews",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHoursTicketEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `OfficeHoursTicket` table"""

    # Name for the events table in the PostgreSQL database
    __tablename__ = "office_hours__ticket"

    # Unique id for OfficeHoursTicket
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Description of ticket, concatenated from user-entered info
    # description: Mapped[str] = mapped_column(String, nullable=False)
    concept_help_description: Mapped[str | None] = mapped_column(String, nullable=True)
    assignment_section_description: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    code_to_english_description: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    concepts_needed_description: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    tactics_tried: Mapped[str | None] = mapped_column(String, nullable=True)
    meeting_summary: Mapped[str | None] = mapped_column(String, nullable=True)
    solutions_used: Mapped[str | None] = mapped_column(String, nullable=True)
    concepts_for_review: Mapped[str | None] = mapped_column(String, nullable=True)
    # Type of OH ticket
    type: Mapped[TicketType] = mapped_column(SQLAlchemyEnum(TicketType), nullable=False)
    # State of OH ticket
    state: Mapped[TicketState] = mapped_column(
        SQLAlchemyEnum(TicketState), default=TicketState.QUEUED, nullable=False
    )
    # Time ticket was created
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    # Time ticket was called by a TA
    called_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True
    )
    # Time ticket was closed by a TA
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True
    )
    # Flag for if UTA has concerns about student
    have_concerns: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Notes from TA
    caller_notes: Mapped[str] = mapped_column(String, default="", nullable=False)

    # One-to-many relationship to event that the ticket was created in
    office_hours_id: Mapped[int] = mapped_column(
        ForeignKey("office_hours.id"), nullable=False
    )
    office_hours: Mapped["OfficeHoursEntity"] = relationship(back_populates="tickets")

    # One-to-many relationship of OfficeHoursTicket to section member(s)
    creators: Mapped[list["SectionMemberEntity"]] = relationship(
        secondary=user_created_tickets_table
    )

    # One-to-one relationship of OfficeHoursTicket to UTA that has called it; optional field
    caller_id: Mapped[int | None] = mapped_column(
        ForeignKey("academics__user_section.id"), nullable=True
    )
    caller: Mapped["SectionMemberEntity"] = relationship(
        back_populates="called_oh_tickets"
    )

    @classmethod
    def from_new_model(cls, model: NewOfficeHoursTicket) -> Self:
        """
        Class method that converts an `NewOfficeHoursTicket` model into a `OfficeHoursTicketEntity`

        Parameters:
            - model (NewOfficeHoursTicket): Model to convert into an entity
        Returns:
            OfficeHoursTicketEntity: Entity created from model
        """
        return cls(
            # we have to update this since the whole codebase relies on this entity file to create ticket objects
            concept_help_description=model.concept_help_description,
            assignment_section_description=model.assignment_section_description,
            code_to_english_description=model.code_to_english_description,
            concepts_needed_description=model.concepts_needed_description,
            tactics_tried=model.tactics_tried,
            # description=model.description,
            type=model.type,
            office_hours_id=model.office_hours_id,
        )

    @classmethod
    def from_model(cls, model: OfficeHoursTicket) -> Self:
        """
        Class method that converts an `OfficeHoursTicket` model into a `OfficeHoursTicketEntity`

        Parameters:
            - model (OfficeHoursTicket): Model to convert into an entity
        Returns:
            OfficeHoursTicketEntity: Entity created from model
        """
        return cls(
            id=model.id,
            # description=model.description,
            type=model.type,
            state=model.state,
            created_at=model.created_at,
            called_at=model.called_at,
            closed_at=model.closed_at,
            have_concerns=model.have_concerns,
            caller_notes=model.caller_notes,
            office_hours_id=model.office_hours_id,
            caller_id=model.caller_id,
        )

    def to_model(self) -> OfficeHoursTicket:
        """
        Converts a `OfficeHoursTicketEntity` object into a `OfficeHoursTicket` model object

        Returns:
            OfficeHoursTicket: `OfficeHoursTicket` object from the entity
        """
        return OfficeHoursTicket(
            id=self.id,
            # description=self.description,
            type=self.type,
            state=self.state,
            created_at=self.created_at,
            called_at=self.called_at,
            closed_at=self.closed_at,
            have_concerns=self.have_concerns,
            caller_notes=self.caller_notes,
            office_hours_id=self.office_hours_id,
            caller_id=self.caller_id,
        )

    def to_details_model(self) -> OfficeHoursTicketDetails:
        """
        Converts a `OfficeHoursTicketEntity` object into a `OfficeHoursTicketDetails` model object

        Returns:
            OfficeHoursTicketDetails: `OfficeHoursTicketDetails` object from the entity
        """
        return OfficeHoursTicketDetails(
            id=self.id,
            # description=self.description,
            type=self.type,
            state=self.state,
            created_at=self.created_at,
            called_at=self.called_at,
            closed_at=self.closed_at,
            have_concerns=self.have_concerns,
            caller_notes=self.caller_notes,
            office_hours_id=self.office_hours_id,
            caller_id=self.caller_id,
            office_hours=self.office_hours,
            creators=[creator.to_flat_model() for creator in self.creators],
            caller=(self.caller.to_flat_model() if self.caller is not None else None),
        )

    # Testing
    @classmethod
    def from_overview_model(cls, model: OfficeHourTicketOverview) -> Self:
        """
        Class method that converts an `OfficeHourTicketOverview` model into a `OfficeHoursEntity`

        Parameters:
            - model (OfficeHourTicketOverview): Model to convert into an entity
        Returns:
            OfficeHoursEntity: Entity created from model
        """
        return cls(
            id=model.id,
            created_at=model.created_at,
            called_at=model.called_at,
            state=TicketState(int(model.state)),
            type=TicketType(int(model.type)),
            concept_help_description=model.concept_help_description,
            assignment_section_description=model.assignment_section_description,
            code_to_english_description=model.code_to_english_description,
            concepts_needed_description=model.concepts_needed_description,
            tactics_tried=model.tactics_tried,
            meeting_summary=model.meeting_summary,
            solutions_used=model.solutions_used,
            concepts_for_review=model.concepts_for_review,
            caller_id=model.caller_id,
            office_hours_id=model.office_hours_id,
        )

    def to_overview_model(self) -> OfficeHourTicketOverview:
        """
        Converts a 'OfficeHoursTicketEntity' object into a 'OfficeHourTicketOverview' model object

        Returns:
            OfficeHourTicketOverview object from the entity
        """

        if self.type == TicketType.CONCEPTUAL_HELP:
            return OfficeHourTicketOverview(
                id=self.id,
                created_at=self.created_at,
                called_at=self.called_at,
                state=(
                    TicketState(self.state).name
                    if not isinstance(self.state, str)
                    else self.state
                ),
                type=(
                    TicketType(self.type).to_string()
                    if not isinstance(self.type, str)
                    else self.type
                ),
                concept_help_description=self.concept_help_description,
                assignment_section_description=None,
                code_to_english_description=None,
                concepts_needed_description=None,
                tactics_tried=self.tactics_tried,
                meeting_summary=self.meeting_summary,
                solutions_used=self.solutions_used,
                concepts_for_review=self.concepts_for_review,
                caller=(
                    # self.caller.to_flat_model() if self.caller is not None else None
                    self.caller.user.to_public_model()
                    if self.caller and self.caller.user
                    else None  # changed this even though it wasnt broken
                ),
                caller_id=self.caller_id,
                office_hours_id=self.office_hours_id,
            )
        else:
            return OfficeHourTicketOverview(
                id=self.id,
                created_at=self.created_at,
                called_at=self.called_at,
                state=(
                    TicketState(self.state).name
                    if not isinstance(self.state, str)
                    else self.state
                ),
                type=(
                    TicketType(self.type).to_string()
                    if not isinstance(self.type, str)
                    else self.type
                ),
                concept_help_description=None,
                assignment_section_description=self.assignment_section_description,
                code_to_english_description=self.code_to_english_description,
                concepts_needed_description=self.concepts_needed_description,
                tactics_tried=self.tactics_tried,
                meeting_summary=self.meeting_summary,
                solutions_used=self.solutions_used,
                concepts_for_review=self.concepts_for_review,
                caller=(
                    self.caller.user.to_public_model()
                    if self.caller and self.caller.user
                    else None
                ),
                caller_id=self.caller_id,
                office_hours_id=self.office_hours_id,
            )

        # return OfficeHourTicketOverview(
        #     id=self.id,
        #     created_at=self.created_at,
        #     called_at=self.called_at,
        #     state=(
        #         TicketState(self.state).name
        #         if not isinstance(self.state, str)
        #         else self.state
        #     ),
        #     type=(
        #         TicketType(self.type).to_string()
        #         if not isinstance(self.type, str)
        #         else self.type
        #     ),
        #     concept_help_description=self.concept_help_description,
        #     assignment_section_description=self.assignment_section_description,
        #     code_to_english_description=self.code_to_english_description,
        #     concepts_needed_description=self.concepts_needed_description,
        #     tactics_tried=self.tactics_tried,
        #     meeting_summary=self.meeting_summary,
        #     solutions_used=self.solutions_used,
        #     concepts_for_review=self.concepts_for_review,
        #     caller=(self.caller.to_flat_model() if self.caller is not None else None),
        # )
