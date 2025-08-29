"""Similar Tickets API

APIs handling see similar tickets function for office hours.
"""

from fastapi import APIRouter, Depends, Path
from typing import Annotated

from backend.models.office_hours.similar_tickets_ai import SimilarTicketsResponse

from ...models.office_hours.office_hours_details import PrimaryOfficeHoursDetails

from ...models.office_hours.office_hours_recurrence_pattern import (
    NewOfficeHoursRecurrencePattern,
)
from ...services.office_hours.office_hours_recurrence import (
    OfficeHoursRecurrenceService,
)
from ...services.office_hours.similar_tickets import OfficeHourSimilarTicketService
from ..authentication import registered_user
from ...services.office_hours.office_hours import OfficeHoursService
from ...models.user import User
from ...models.office_hours.office_hours import OfficeHours, NewOfficeHours
from ...models.academics.my_courses import (
    OfficeHourQueueOverview,
    OfficeHourEventRoleOverview,
    OfficeHourGetHelpOverview,
)

__authors__ = ["Riley Chapman, Sarah Glenn"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"

api = APIRouter(prefix="/api/office-hours/ticket")


@api.post(
    "/{id}/similar",
    summary="Find similar office hours tickets",
    description="Use AI to search through past tickets and retrieve those that are most similar to the currently open ticket.",
    responses={
        404: {
            "description": "Ticket not found - The provided ticket ID does not exist."
        },
        200: {"description": "Success - Similar tickets were found and returned."},
    },
    tags=["Office Hours"],
)
def get_similar_tickets(
    id: Annotated[
        int,
        Path(
            description="The ID of the current open ticket for which similar tickets should be found.",
            examples=[1, 2],
        ),
    ],
    subject: User = Depends(registered_user),
    oh_ticket_svc: OfficeHourSimilarTicketService = Depends(),
) -> SimilarTicketsResponse:
    """
    Uses AI to search through past tickets to find those that are similar to the open ticket.

    Args:
        id (int): ID of the current open ticket.
        subject (User): The user requesting the similar tickets.
        oh_ticket_svc (OfficeHourSimilarTicketService): The injected service layer.

    Returns:
        SimilarTicketsResponse: List of similar tickets

    """
    return oh_ticket_svc.find_similar_tickets(subject, id)
