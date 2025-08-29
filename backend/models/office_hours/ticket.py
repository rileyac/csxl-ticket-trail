from pydantic import BaseModel
from datetime import datetime

from .ticket_type import TicketType
from .ticket_state import TicketState

__authors__ = [
    "Ajay Gandecha",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
    "Maddy Andrews",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class NewOfficeHoursTicket(BaseModel):
    """
    Pydantic model to represent a new ticket.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    # I added these in here because we want to store them when the student creates the ticket. This is the model they see so
    # we should have the fields ready to be inhabited at this point.
    concept_help_description: str | None = None  # conceptual help
    assignment_section_description: str | None = None  # assignment help
    code_to_english_description: str | None = None  # assignment help
    concepts_needed_description: str | None = None  # assignment help
    tactics_tried: str | None = None  # assignment help
    # description: str | None = None  # TODO: remove any trace from existence
    type: TicketType
    office_hours_id: int


class OfficeHoursTicket(NewOfficeHoursTicket):
    """
    Pydantic model to represent an `OfficeHoursTicket`.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    id: int
    state: TicketState = TicketState.QUEUED
    created_at: datetime = datetime.now()
    called_at: datetime | None
    closed_at: datetime | None
    have_concerns: bool = False
    caller_notes: str = ""
    caller_id: int | None
    # description: str | None = None
    concept_help_description: str | None = None  # conceptual help
    assignment_section_description: str | None = None  # assignment help
    code_to_english_description: str | None = None  # assignment help
    concepts_needed_description: str | None = None  # assignment help
    tactics_tried: str | None = None  # assignment help
    meeting_summary: str | None = None  # TA response
    solutions_used: str | None = None  # TA response
    concepts_for_review: str | None = None  # TA response


class OfficeHoursTicketTAResponse(BaseModel):
    """
    Pydantic model to represent an `OfficeHoursTicket`.

    This model is ALSO based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database. It updates the ticket
    in the db upon the TA closing the ticket.


    """

    meeting_summary: str | None = None  # TA response
    solutions_used: str | None = None  # TA response
    concepts_for_review: str | None = None
