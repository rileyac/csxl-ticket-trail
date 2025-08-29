"""Office Hours API

APIs handling office hours.
"""

from fastapi import APIRouter, Depends, Body
from typing import Annotated
from ..authentication import registered_user
from ...services.office_hours.ticket import OfficeHourTicketService
from ...models.user import User
from ...models.office_hours.ticket import (
    NewOfficeHoursTicket,
    OfficeHoursTicket,
    OfficeHoursTicketTAResponse,
)

from ...models.academics.my_courses import OfficeHourTicketOverview

__authors__ = [
    "Ajay Gandecha",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
    "Maddy Andrews",
    "Jack Coury",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/office-hours/ticket")


@api.put(
    "/{id}/call",
    summary="Call a ticket",
    description="accesses a ticket in the DB via its ticket id and returns the overview object to be populate the frontend.",
    responses={
        403: {
            "description": "Forbidden - You do not have permission to call this ticket."
        },
        404: {"description": "Not Found - The ticket does not exist."},
    },
    tags=["Office Hours"],
)
def call_ticket(
    id: int,
    subject: User = Depends(registered_user),
    oh_ticket_svc: OfficeHourTicketService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Calls a ticket in an office hour queue.

    Returns:
        OfficeHourTicketOverview: OH ticket called
    """
    return oh_ticket_svc.call_ticket(subject, id)


@api.put("/{id}/cancel", tags=["Office Hours"])
def cancel_ticket(
    id: int,
    subject: User = Depends(registered_user),
    oh_ticket_svc: OfficeHourTicketService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Cancels a ticket in an office hour queue.

    Returns:
        OfficeHourTicketOverview: OH Ticket canceled
    """
    return oh_ticket_svc.cancel_ticket(subject, id)


@api.put(
    "/{id}/close",
    summary="close a ticket",
    description="closes a ticket after TA student interaction and stores TA data in DB.",
    responses={
        403: {
            "description": "Forbidden - You do not have permission to close this ticket."
        },
        404: {"description": "Not Found - The ticket does not exist."},
    },
    tags=["Office Hours"],
)
def close_ticket(
    id: int,
    ticket_data: Annotated[
        OfficeHoursTicketTAResponse,
        Body(
            description="Responses entered by the TA when closing a ticket.",
            openapi_examples={
                "example": {
                    "summary": "Example TA Response",
                    "description": "Basic example filling out the TA meeting summary and tools used.",
                    "value": {
                        "meeting_summary": "Student was confused about list indexing, we memory diagrammed examples.",
                        "solutions_used": "Explained len(), range(), and list indexing with diagrams.",
                        "concepts_for_review": "for loops, subscription notation",
                    },
                }
            },
        ),
    ],
    subject: User = Depends(registered_user),
    oh_ticket_svc: OfficeHourTicketService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Closes a ticket in an office hour queue.

    Args:
        id (int): The ID of the ticket being closed.
        ticket_data (OfficeHoursTicketTAResponse): The filled out TA forms to be set in the DB.
        subject (User): The user closing the ticket.
        oh_ticker_svc (OfficeHourTicketService): The injected service layer.

    Returns:
        OfficeHourTicketOverview: OH Ticket closed with updated fields
    """
    return oh_ticket_svc.close_ticket(subject, id, ticket_data)


@api.post(
    "/",
    summary="Create a new office hours ticket",
    description="Submit a new office hours ticket to the database with student information.",
    responses={
        400: {"description": "Invalid input - Ticket could not be created"},
        200: {"description": "Created - Ticket successfully added to the database"},
    },
    tags=["Office Hours"],
)
def new_oh_ticket(
    ticket: Annotated[
        NewOfficeHoursTicket,
        Body(
            description="The student input for a newly created office hours ticket.",
            openapi_examples={
                "assignment_ticket_example": {
                    "summary": "Assignment Help Ticket",
                    "description": "Ticket option for assignment help",
                    "value": {
                        "type": "ASSIGNMENT_HELP",
                        "office_hours_id": 1,
                        "assignment_section_description": "Working on part 2 of assignment 3, need help with the loop.",
                        "code_to_english_description": "Explain what this loop is doing.",
                        "concepts_needed_description": "for loops, list indexing",
                        "tactics_tried": "Checked class notes and Googled syntax.",
                    },
                },
                "conceptual_ticket_example": {
                    "summary": "Conceptual Help Ticket",
                    "description": "Ticket option for conceptual questions.",
                    "value": {
                        "type": "CONCEPTUAL_HELP",
                        "office_hours_id": 1,
                        "concept_help_description": "Need clarification on how recursion works.",
                    },
                },
            },
        ),
    ],
    subject: User = Depends(registered_user),
    oh_ticket_svc: OfficeHourTicketService = Depends(),
) -> OfficeHourTicketOverview:
    """
    Adds a new OH ticket to the database.

    Returns:
        OfficeHoursTicketOverview: OH Ticket created
    """
    return oh_ticket_svc.create_ticket(subject, ticket)
