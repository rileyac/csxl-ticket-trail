from fastapi import Depends
from backend.models.academics.my_courses import OfficeHourTicketOverview
from backend.models.office_hours.similar_tickets_ai import (
    SimilarTicketsAIResponse,
    SimilarTicketsResponse,
)
from backend.services.openai import OpenAIService


class SimilarTicketAIService:
    """
    Service layer that injects OpenAiService to make the Open AI call to fetch similar tickets.
    """

    def __init__(self, openai: OpenAIService = Depends()):
        """
        Initializes OpenAI Service.
        """

        self._openai = openai

    def ai_for_similar_tickets(
        self, prompt_input: dict[str, str], past_tickets: list[OfficeHourTicketOverview]
    ) -> SimilarTicketsAIResponse:
        """
        Makes a call to the OpenAI Service to fetch similar tickets.

        Args:
            prompt_input (dict[str, str]): Fields of current open ticket.
            past_tickets (list[OfficeHourTicketOverview]): All of the past tickets to be searched through by AI.

        Returns:
            SimilarTicketsAIResponse: List of ticket ID's that AI deemed as simiar to current ticket.
        """

        system_prompt = "You are an AI assistant helping a team with office hours by finding past office hours tickets that are either conceptually similar or have similar issues to a current one. Return a list of ticket ids that are similar to the one given."

        # passing to the build prompt method prompt_input as the current ticket
        user_prompt = self._build_prompt(prompt_input, past_tickets)

        return self._openai.prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            # expects a list of ids
            response_model=SimilarTicketsAIResponse,
        )

    # takes the info prepared by similar tickets service and makes those into suitable format for AI
    def _build_prompt(
        self,
        current_ticket: dict[str, str | None],
        past_tickets: list[OfficeHourTicketOverview],
    ) -> str:
        """
        Helper function to build user prompt for AI call.

        Args:
            current_tickets: (dict[str, str | None]): Fields of current open ticket.
            past_tickets (list[OfficeHourTicketOverview]): All of the past tickets to be searched through by AI.

        Returns:
            str: A string that contains the current ticket fields as well as all of the info about all past tickets.
        """
        prompt = "Current Ticket:\n"
        for k, v in current_ticket.items():
            if v:
                prompt += f"{k}: {v}\n"

        prompt += "\nPast Tickets:\n"
        for t in past_tickets:
            if t.type == "Conceptual Help":
                prompt += (
                    f"ID: {t.id}\n"
                    f"Concept Help Description: {t.concept_help_description}\n"
                    f"Tactics Tried: {t.tactics_tried}\n"
                    f"Meeting Summary: {t.meeting_summary}\n"
                    f"Solutions and Tools Used: {t.solutions_used}\n"
                    f"Concepts for Review: {t.concepts_for_review}\n"  # do we want this?
                    "---\n"
                )
            else:
                prompt += (
                    f"ID: {t.id}\n"
                    f"Assignment Help Description: {t.assignment_section_description}\n"
                    f"Code to English: {t.code_to_english_description}\n"
                    f"Concepts Needed: {t.concepts_needed_description}\n"
                    f"Tactics Tried: {t.tactics_tried}\n"
                    f"Meeting Summary: {t.meeting_summary}\n"
                    f"Solutions and Tools Used: {t.solutions_used}\n"
                    f"Concepts for Review: {t.concepts_for_review}\n"  # do we want this?
                    "---\n"
                )

        prompt += '\nReturn a JSON object like: { "similar_ticket_ids": [3, 12, 17] }'
        print(prompt)
        return prompt
