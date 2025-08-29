"""Tests for AI Integration."""

from os import getenv
from openai import AzureOpenAI
import pytest
from unittest.mock import MagicMock, Mock

from backend.entities.academics.section_member_entity import SectionMemberEntity
from backend.models.roster_role import RosterRole
from backend.services.office_hours.similar_tickets import OfficeHourSimilarTicketService
from backend.services.openai import OpenAIService

from ....services.exceptions import CoursePermissionException, ResourceNotFoundException

# Import the fake model data in a namespace for test assertions
from .. import user_data
from ..office_hours import office_hours_data

from unittest.mock import patch
from backend.main import app
from backend.models.office_hours.similar_tickets_ai import (
    SimilarTicketsAIResponse,
    SimilarTicketsResponse,
)
from backend.models.academics.my_courses import OfficeHourTicketOverview
from backend.services.office_hours.similar_tickets_ai import SimilarTicketAIService
from sqlalchemy.orm import Session


__authors__ = ["Riley Chapman"]
__copyright__ = "Copyright 2025"


# Similar Ticket SVC Unit Tests


def test_get_similar_tickets_valid():
    """Ensures similar tickets are returned when user has permission and a valid ticket ID is given."""
    mock_session = Mock(spec=Session)
    mock_ai_svc = MagicMock()
    ticket_svc = OfficeHourSimilarTicketService(
        session=mock_session, ai_service=mock_ai_svc
    )

    current_ticket = office_hours_data.comp_110_called_ticket
    user = user_data.instructor

    # Mock AI service response with a SimilarTicketsAIResponse
    mock_ai_response = MagicMock()
    mock_ai_response.similar_ticket_ids = [
        office_hours_data.comp_110_closed_ticket_1.id,
        office_hours_data.comp_110_closed_ticket_2.id,
    ]
    mock_ai_svc.ai_for_similar_tickets.return_value = mock_ai_response

    # Mock the session to return closed tickets
    mock_entity_1 = Mock()
    mock_entity_1.to_overview_model.return_value = (
        office_hours_data.comp_110_closed_ticket_1
    )

    mock_entity_2 = Mock()
    mock_entity_2.to_overview_model.return_value = (
        office_hours_data.comp_110_closed_ticket_2
    )

    # Ensuring that scalars().all() returns a list of mock entities
    # Simulates a database query that returns two ticket entities.
    mock_session.scalars.return_value.all.return_value = [mock_entity_1, mock_entity_2]

    # Mock the permission check (simulating that the user is a valid TA or Instructor for the course)
    mock_user_member = Mock(spec=SectionMemberEntity)
    mock_user_member.user_id = user.id
    mock_user_member.member_role = RosterRole.INSTRUCTOR  # Simulating instructor role
    mock_session.scalars.return_value.unique.return_value.all.return_value = [
        mock_user_member
    ]

    result: SimilarTicketsResponse = ticket_svc.find_similar_tickets(
        subject=user, id=current_ticket.id
    )

    assert len(result.similar_tickets) == 2
    assert all(isinstance(t, OfficeHourTicketOverview) for t in result.similar_tickets)


def test_get_similar_tickets_no_similar():
    """Ensures no similar tickets are returned when the AI service returns no matches."""
    mock_session = Mock(spec=Session)
    mock_ai_svc = MagicMock()
    ticket_svc = OfficeHourSimilarTicketService(
        session=mock_session, ai_service=mock_ai_svc
    )

    current_ticket = office_hours_data.comp_110_called_ticket
    user = user_data.instructor

    # Mock AI service response with no similar tickets
    mock_ai_response = MagicMock()
    mock_ai_response.similar_ticket_ids = []
    mock_ai_svc.ai_for_similar_tickets.return_value = mock_ai_response

    # Mock the session to return an empty list
    mock_session.scalars.return_value.all.return_value = []

    # Mock the permission check (simulating that the user is a valid TA or Instructor for the course)
    mock_user_member = Mock(spec=SectionMemberEntity)
    mock_user_member.user_id = user.id
    mock_user_member.member_role = RosterRole.INSTRUCTOR  # Simulating instructor role
    mock_session.scalars.return_value.unique.return_value.all.return_value = [
        mock_user_member
    ]

    result: SimilarTicketsResponse = ticket_svc.find_similar_tickets(
        subject=user, id=current_ticket.id
    )

    assert len(result.similar_tickets) == 0  # No similar tickets should be found


def test_get_similar_tickets_invalid_ticket_id():
    """Ensures an exception is raised when an invalid ticket ID is provided."""
    mock_session = Mock(spec=Session)
    mock_ai_svc = MagicMock()
    ticket_svc = OfficeHourSimilarTicketService(
        session=mock_session, ai_service=mock_ai_svc
    )

    user = user_data.instructor

    # Simulate invalid ticket ID by returning None for the ticket entity
    mock_session.get.return_value = None

    # Test that the method raises ResourceNotFoundException when no ticket is found
    with pytest.raises(ResourceNotFoundException):
        ticket_svc.find_similar_tickets(subject=user, id=999)  # Invalid ID


def test_get_similar_tickets_permission_denied():
    """Ensures a permission exception is raised when a user doesn't have access to view similar tickets."""

    mock_session = Mock(spec=Session)
    mock_ai_svc = MagicMock()
    ticket_svc = OfficeHourSimilarTicketService(
        session=mock_session, ai_service=mock_ai_svc
    )

    current_ticket = office_hours_data.comp_110_called_ticket
    user = user_data.student  # Simulate a student who doesn't have permission

    # Mock the query to return the student as part of the class
    mock_user_member = Mock(spec=SectionMemberEntity)
    mock_user_member.member_role = RosterRole.STUDENT  # Simulate a student member role

    # Mock the session to return the student member
    mock_session.scalars.return_value.unique.return_value.all.return_value = [
        mock_user_member
    ]

    # Ensure that the permission exception is raised when the student tries to access the similar tickets
    with pytest.raises(CoursePermissionException):
        ticket_svc.find_similar_tickets(subject=user, id=current_ticket.id)


def test_get_similar_tickets_ta_permission():
    """Ensures a TA has permission to access similar tickets."""

    mock_session = Mock(spec=Session)
    mock_ai_svc = MagicMock()
    ticket_svc = OfficeHourSimilarTicketService(
        session=mock_session, ai_service=mock_ai_svc
    )

    current_ticket = office_hours_data.comp_110_called_ticket
    user = user_data.uta  # Simulate a TA with permission

    # Mock AI service response with similar tickets
    mock_ai_response = MagicMock()
    mock_ai_response.similar_ticket_ids = [
        office_hours_data.comp_110_closed_ticket_1.id,
        office_hours_data.comp_110_closed_ticket_2.id,
    ]
    mock_ai_svc.ai_for_similar_tickets.return_value = mock_ai_response

    # Mock the session to return closed tickets
    mock_entity_1 = Mock()
    mock_entity_1.to_overview_model.return_value = (
        office_hours_data.comp_110_closed_ticket_1
    )

    mock_entity_2 = Mock()
    mock_entity_2.to_overview_model.return_value = (
        office_hours_data.comp_110_closed_ticket_2
    )

    # Ensuring that scalars().all() returns a list of mock entities
    mock_session.scalars.return_value.all.return_value = [mock_entity_1, mock_entity_2]

    # Mock the permission check (simulating that the user is a TA)
    mock_user_member = Mock(spec=SectionMemberEntity)
    mock_user_member.user_id = user.id
    mock_user_member.member_role = RosterRole.UTA  # Simulating TA role
    mock_session.scalars.return_value.unique.return_value.all.return_value = [
        mock_user_member
    ]

    result: SimilarTicketsResponse = ticket_svc.find_similar_tickets(
        subject=user, id=current_ticket.id
    )

    assert len(result.similar_tickets) == 2
    assert all(isinstance(t, OfficeHourTicketOverview) for t in result.similar_tickets)


# Similar Tickets AI SVC Test


def test_ai_for_similar_tickets_success():
    """Test that AI service returns similar ticket IDs as expected."""

    mock_openai_service = MagicMock(spec=OpenAIService)
    ticket_svc = SimilarTicketAIService(openai=mock_openai_service)

    # Using existing ticket data
    current_ticket = office_hours_data.comp_110_called_ticket
    prompt_input = {
        "assignment_section_description": current_ticket.assignment_section_description,
        "code_to_english_description": current_ticket.code_to_english_description,
        "concepts_needed_description": current_ticket.concepts_needed_description,
        "tactics_tried": current_ticket.tactics_tried,
    }

    past_tickets = [
        office_hours_data.comp_110_closed_ticket_1,
        office_hours_data.comp_110_closed_ticket_2,
    ]

    # Mock the AI service response
    mock_ai_response = MagicMock(spec=SimilarTicketsAIResponse)
    mock_ai_response.similar_ticket_ids = [1, 2]
    mock_openai_service.prompt.return_value = mock_ai_response

    result = ticket_svc.ai_for_similar_tickets(prompt_input, past_tickets)

    assert len(result.similar_ticket_ids) == 2
    assert result.similar_ticket_ids == [1, 2]
    mock_openai_service.prompt.assert_called_once_with(
        system_prompt="You are an AI assistant helping a team with office hours by finding past office hours tickets that are either conceptually similar or have similar issues to a current one. Return a list of ticket ids that are similar to the one given.",
        user_prompt=(
            f"Current Ticket:\n"
            f"assignment_section_description: {current_ticket.assignment_section_description}\n"
            f"code_to_english_description: {current_ticket.code_to_english_description}\n"
            f"concepts_needed_description: {current_ticket.concepts_needed_description}\n"
            f"tactics_tried: {current_ticket.tactics_tried}\n"
            "\nPast Tickets:\n"
            f"ID: {office_hours_data.comp_110_closed_ticket_1.id}\n"
            f"Assignment Help Description: {office_hours_data.comp_110_closed_ticket_1.assignment_section_description}\n"
            f"Code to English: {office_hours_data.comp_110_closed_ticket_1.code_to_english_description}\n"
            f"Concepts Needed: {office_hours_data.comp_110_closed_ticket_1.concepts_needed_description}\n"
            f"Tactics Tried: {office_hours_data.comp_110_closed_ticket_1.tactics_tried}\n"
            f"Meeting Summary: {office_hours_data.comp_110_closed_ticket_1.meeting_summary}\n"
            f"Solutions and Tools Used: {office_hours_data.comp_110_closed_ticket_1.solutions_used}\n"
            f"Concepts for Review: {office_hours_data.comp_110_closed_ticket_1.concepts_for_review}\n"
            "---\n"
            f"ID: {office_hours_data.comp_110_closed_ticket_2.id}\n"
            f"Assignment Help Description: {office_hours_data.comp_110_closed_ticket_2.assignment_section_description}\n"
            f"Code to English: {office_hours_data.comp_110_closed_ticket_2.code_to_english_description}\n"
            f"Concepts Needed: {office_hours_data.comp_110_closed_ticket_2.concepts_needed_description}\n"
            f"Tactics Tried: {office_hours_data.comp_110_closed_ticket_2.tactics_tried}\n"
            f"Meeting Summary: {office_hours_data.comp_110_closed_ticket_2.meeting_summary}\n"
            f"Solutions and Tools Used: {office_hours_data.comp_110_closed_ticket_2.solutions_used}\n"
            f"Concepts for Review: {office_hours_data.comp_110_closed_ticket_2.concepts_for_review}\n"
            "---\n"
            '\nReturn a JSON object like: { "similar_ticket_ids": [3, 12, 17] }'
        ),
        response_model=SimilarTicketsAIResponse,
    )


def test_ai_for_similar_tickets_no_matches():
    """Test that AI service returns no similar ticket IDs when no matches are found."""

    # Mock the OpenAI service
    mock_openai_service = MagicMock(spec=OpenAIService)
    ticket_svc = SimilarTicketAIService(openai=mock_openai_service)

    # Use existing ticket data
    current_ticket = office_hours_data.comp_110_called_ticket
    prompt_input = {
        "assignment_section_description": current_ticket.assignment_section_description,
        "code_to_english_description": current_ticket.code_to_english_description,
        "concepts_needed_description": current_ticket.concepts_needed_description,
        "tactics_tried": current_ticket.tactics_tried,
    }
    past_tickets = [
        office_hours_data.comp_110_closed_ticket_1,
        office_hours_data.comp_110_closed_ticket_2,
    ]

    # Mock the AI service response with no similar tickets
    mock_ai_response = MagicMock(spec=SimilarTicketsAIResponse)
    mock_ai_response.similar_ticket_ids = []
    mock_openai_service.prompt.return_value = mock_ai_response

    # Call the method under test
    result = ticket_svc.ai_for_similar_tickets(prompt_input, past_tickets)

    assert result.similar_ticket_ids == []  # No similar tickets


def test_ai_for_similar_tickets_no_past_tickets():
    """Test that AI service handles an empty list of past tickets gracefully."""

    # Mock the OpenAI service
    mock_openai_service = MagicMock(spec=OpenAIService)
    ticket_svc = SimilarTicketAIService(openai=mock_openai_service)

    # Use existing ticket data
    current_ticket = office_hours_data.comp_110_called_ticket
    prompt_input = {
        "assignment_section_description": current_ticket.assignment_section_description,
        "code_to_english_description": current_ticket.code_to_english_description,
        "concepts_needed_description": current_ticket.concepts_needed_description,
        "tactics_tried": current_ticket.tactics_tried,
    }
    past_tickets = []  # No past tickets

    # Mock the AI service response with no similar tickets
    mock_ai_response = MagicMock(spec=SimilarTicketsAIResponse)
    mock_ai_response.similar_ticket_ids = []
    mock_openai_service.prompt.return_value = mock_ai_response

    # Call the method under test
    result = ticket_svc.ai_for_similar_tickets(prompt_input, past_tickets)

    assert (
        result.similar_ticket_ids == []
    )  # No similar tickets when no past tickets exist


# E2E AI Integration test


def test_real_openai_integration_with_fixture_data():
    """Sends real ticket data to OpenAI and sends it back to service."""
    # Manually create client
    client = AzureOpenAI(
        api_key=getenv("UNC_OPENAI_API_KEY"),
        api_version=getenv("UNC_OPENAI_API_VERSION", default="2024-10-21"),
        azure_endpoint=getenv(
            "UNC_OPENAI_API_ENDPOINT", default="https://azureaiapi.cloud.unc.edu"
        ),
    )

    openai_svc = OpenAIService(client=client)
    ai_svc = SimilarTicketAIService(openai=openai_svc)

    current_ticket = office_hours_data.red_black_called_ticket

    prompt_input = {
        "assignment_section_description": current_ticket.assignment_section_description,
        "code_to_english_description": current_ticket.code_to_english_description,
        "concepts_needed_description": current_ticket.concepts_needed_description,
        "tactics_tried": current_ticket.tactics_tried,
    }

    past_tickets = [
        office_hours_data.comp_110_closed_ticket_RB1,
        office_hours_data.comp_110_closed_ticket_RB2,
        office_hours_data.comp_110_closed_ticket_RB3,
        office_hours_data.comp_110_closed_ticket_RB4,
        office_hours_data.comp_110_closed_ticket_RB5,
        office_hours_data.comp_110_closed_ticket_unrelated,
    ]

    response: SimilarTicketsAIResponse = ai_svc.ai_for_similar_tickets(
        prompt_input, past_tickets
    )

    assert isinstance(response.similar_ticket_ids, list)
    assert all(isinstance(tid, int) for tid in response.similar_ticket_ids)
    assert len(response.similar_ticket_ids) > 0
    print("response here:", response)
    assert 21 not in response.similar_ticket_ids
