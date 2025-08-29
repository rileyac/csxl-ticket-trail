from pydantic import BaseModel
from backend.models.academics.my_courses import OfficeHourTicketOverview
from typing import List

__authors__ = ["Riley Chapman", "Sarah Glenn"]

"""
Pydantic models to represent responses for Similar Ticket service calls.
"""


class SimilarTicketsResponse(BaseModel):
    """
    Pydantic model to represent a response from the Similar Ticket Service Layer.
    """

    similar_tickets: List[OfficeHourTicketOverview]


class SimilarTicketsAIResponse(BaseModel):
    """
    Pydantic model to represent a response from the Similar Ticket OpenAI Service Layer.
    """

    similar_ticket_ids: List[int]
