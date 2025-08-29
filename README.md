# Ticket Trail: Leveraging Student Support History
## COMP 423 Project

Authors:
[Sarah Glenn](https://github.com/skglenn07), [Taylor Morris](https://github.com/Taylor1515), [Riley Chapman](https://github.com/rileyac), [Jack Coury](https://github.com/jcoury89)

## Overview

While working as a TA, students often come in with issues other students have brought up in the past. Unfortunately, the CSXL website does not currently have a utility for storing or accessing past solutions to student problems. Our project aims to solve this. First, when a TA calls a ticket, they will be prompted to add a brief summary of their meeting with the student as well as information about how they solved problems. Additionally, AI will be utilized to search through previous tickets for similar issues, and the TA responses from these tickets will be presented to the TA for them to reference. This will provide the TA with vital context and improve the efficiency of office hours meetings.

## Key Persona

**Teresa TA:** Teresa is a teaching assistant for a Computer Science course at UNC. She wants to help students as efficiently as possible, but she is only human. She doesn't necessarily have answers to every problem she encounters. From issues with setup to explaining concepts in novel ways to a student that is struggling, having access to other TA solutions would help Teresa better assist students and expedite ticket progression. With our new feature, Teresa TA would not only be able to contribute to a database of TA responses, but also be able to crowdsource solutions from previous interactions, via LLM filtering of a TA response collection.

## User Stories

### Story 1

As Teresa TA, I want to contribute to a ticket solutions database so that fellow TA’s, instructors, and I can draw upon it in the future.

_Acceptance Criteria:_

- I want a response form to be included in a ticket I have called (while the ticket is open).
- I want the response form to include sections related to problem summary, solutions and concepts for review.
- Upon completion of student interaction, I want to submit a ticket with a response form to a database that can be accessed by other TA’s.

### Story 2

As Teresa TA, I want to click on a button that has a LLM sort through tickets, pulling out tickets similar to mine based on problem descriptions, so that I can draw upon previous interactions in order to better assist a student.

_Acceptance Criteria:_

- I want a button included in the TA response portion of a ticket that has an LLM generate this collection of tickets.
- Upon clicking this button, I want a new page brought up that shows all tickets related to the ticket I’m currently working on.

## Office Hours Ticket API

`backend/api/office_hours/ticket.py`

_All endpoints require authentication as a registered user._

### 1. `POST /api/office-hours/ticket/`

**Description**:

Creates a new ticket in the office hours queue.

**Path Parameters**:

- `ticket` (NewOfficeHoursTicket): The new office hours ticket to be created

**Service Layer**:

Uses the OfficeHourTicketService, and calls `create_ticket(subject, ticket)`, which adds the new ticket to the database with the student-entered fields.
The underlying data model is defined in `backend/entities/office_hours/ticket_entity.py` under the class OfficeHoursTicketEntity.

**Returns**:

Returns the created ticket as an OfficeHourTicketOverview.

## ![Alt text](images/ticket_trail/assignment_ticket_start.png)

## ![Alt text](images/ticket_trail/conceptual_ticket_start.png)

### 2. `PUT /api/office-hours/ticket/{id}/call`

**Description**:

Calls a ticket in an office hours queue.

**Path Parameters**:

- `id` (int): The ID of the ticket to call.

**Service layer:**

Uses the OfficeHourTicketService, and calls `call_ticket(subject, id)`, which updates certain fields in the database to make the current ticket reflect a called ticket.

**Returns**:

The called ticket as an OfficeHourTicketOverview.

### 3. `PUT /api/office-hours/ticket/{id}/close`

**Description**:

Closes a ticket in an office hours queue.

**Path Parameters**:

- `id` (int): The ID of the ticket to call.

**Service layer:**

Uses the OfficeHourTicketService, and calls `close_ticket(subject, id)`, which updates certain fields in the database to make the current ticket reflects a fully closed ticket.

**Returns**:

The closed ticket as an OfficeHourTicketOverview.

### 4. `PUT /api/office-hours/ticket/{id}/cancel`

**Description**:

Cancels a ticket in an office hours queue.

**Path Parameters**:

- `id` (int): The ID of the ticket to call.

**Service layer:**

Uses the OfficeHourTicketService, and calls `cancel_ticket(subject, id)`, which changes the 'state' field of the ticket to CANCELED in the database.

**Returns**:

The cancelled ticket as an OfficeHourTicketOverview.

### Models

`NewOfficeHoursTicket`

Represents a newly created office hours ticket, which is essentially is a subset of fields from a complete ticket. Includes the student entered fields upon creating the ticket.

`OfficeHourTicketOverview`

Represents an office hour ticket in its entirety. Based on the OfficeHoursTicketEntity model, which defines the shape of the OfficeHoursTicket database in the PostgreSQL database. Includes both student and TA entered fields, as well as information about the ticket itself (assignment vs. conceptual help, when it was called, who it was called by, etc). Upon calling a ticket, the student fields are populated in the database. TA portions are populated upon closing a ticket.

`OfficeHoursTicketTAResponse`

Represents the TA portion of an office hour ticket. It is submitted to the api call upon closing the ticket and is fed into the postgresSQL database upon closing the ticket.

## Called Ticket Card Widget

`frontend/src/app/my-courses/course/office-hours/widgets/called-ticket-card`

### Overview

The Called Ticket Card Widget is responsible for displaying and interacting with a ticket once it has been called during an office hours session.  
This widget provides both a view of the students’ submitted information and an interface for the TA to record their meeting summary, solutions used, and any concepts the student should review.  
It also provides a method to navigate to similar past tickets through AI filtering.

## ![Alt text](images/ticket_trail/TA_response_fields.png)

### Behavior

When a student completes their input for the already built **queued-ticket-card** widget, the information gets passed into the **called-ticket-card** widget (and also stored in the Postgres database, see below).  
What we added was the **TA response form**, which provides fields.  
The TA must provide input for at least the first two fields before closing the ticket becomes an option.  
They may also press the **See Similar Tickets** button in order to navigate to the ticket summary page and view previous tickets with similar issues.

### Models

This widget employs the modified `OfficeHoursTicketOverview` model to access student fields, and then uses the newly created `OfficeHoursTicketTAResponse` model to submit TA responses upon closing the ticket.

### Services

We completed implementation of Postgres databasing for the **queued-ticket-card** widget, so now when a TA calls their ticket it submits the student’s info to the database via the `my-courses.service` method, `callTicket`, which calls the `PUT` method in the API.  
When closing the ticket, the TA invokes the `closeTicket` method, which passes the `OfficeHoursTicketTAResponse` object to the `PUT` method in the API.

## Ticket Summary Card Widget

`frontend/src/app/my-courses/course/office-hours/widgets/ticket-summary-card`

### Overview

The Ticket Summary Card Widget is responsible for displaying a summarized view of a previously closed office hours ticket.  
This widget shows both the TA’s recorded meeting summary and the solutions used to resolve the ticket.  
It also provides the ability to reveal additional fields the student originally filled out, by toggling the **See More** button.

## ![Alt text](images/ticket_trail/summar_ticket_card_maximized.png)

### Behavior

When a TA clicks the **See More** button, the widget expands to display the original ticket information fields, including concept help, assignment description, and tactics tried.  
Otherwise, only the meeting summary and solutions used are shown by default.

### Models

This widget uses the `OfficeHourTicketOverview` model to access all necessary ticket information, both from the student and TA portions.

### Services

This widget does not directly call backend services.  
It instead depends on its parent component, `similar-tickets-page`, to provide it with an `OfficeHourTicketOverview` object to populate it.

## Similar Tickets Page

`frontend/src/app/my-courses/course/office-hours/similar-tickets-page`

### Overview

The Similar Tickets Page is responsible for displaying a collection of previously closed office hours tickets that are similar to the currently called ticket.  
This page allows the TA to review past student issues and TA solutions that may help them solve the problem at hand more efficiently.

## ![Alt text](images/ticket_trail/similar_tickets_page.png)

### Behavior

When the TA clicks the **See Similar Tickets** button from the called-ticket-card widget, the frontend routes them to this page.  
The ticket ID of the currently called ticket is passed through the URL, and the page fetches similar tickets from the backend via the `seeSimilarTickets` method inside the `my-courses.service`.  
If no similar tickets are found, a "No similar tickets found" message is displayed.  
Otherwise, each similar ticket is displayed using a ticket-summary-card widget inside a grid layout.

### Models

This page uses the `OfficeHourTicketOverview` model for each similar ticket that is displayed.

### Services

This page calls the `seeSimilarTickets` method from the `MyCoursesService` to request similar tickets from the API's post method, `get_similar_tickets`. This is the entrypoint for our AI integration.

## AI Integration

### AI Integration API

`backend/api/office_hours/similar_tickets.py`

#### `POST /api/office-hours/ticket/{id}/similar`

**Description**:

Uses AI to search through past tickets to find those that are similar to the open ticket.

**Path Parameters**:

- `id` (int): The ID of the current open ticket.

**Service Layer:**

There are three layers of services involved in finding similar office hour tickets using AI: `OfficeHourSimilarTicketService`, `SimilarTicketAIService`, and `OpenAIService`.

First, the API uses the `OfficeHourSimilarTicketService` and calls `find_similar_tickets(subject, id)`:

- Fetches the current ticket from the database.
- Builds an input dictionary (`prompt_input`) based on the ticket's fields.
- Compiles a list of all closed past tickets.

Then, `OfficeHourSimilarTicketService` uses `SimilarTicketAIService` and calls `ai_for_similar_tickets(prompt_input, past_tickets)`:

- Builds a user prompt combining the current ticket and all past tickets.
- Sends the prompt to `OpenAIService`, which uses OpenAI to find similar ticket IDs.
- Returns a `SimilarTicketsAIResponse` back to `OfficeHourSimilarTicketService`.

Finally, back in `OfficeHourSimilarTicketService`:

- Filters and fetches the corresponding tickets from the database by ID.

**Returns**:

Returns the list of similar tickets in a `SimilarTicketsResponse`.

### Models

`SimilarTicketsResponse`

Pydantic model to represent a response from the Similar Ticket Service Layer, which is a list of OfficeHourTicketOverview obects.

`SimilarTicketsAIResponse`

Pydantic model to represent a response from the Similar Ticket OpenAI Service Layer, which is a list of ticket ID's as integers.

## Full Stack Summary

### Backend

| **File**                                                                                                     | **Description**                                                                                                                                                                        |
| :----------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `backend/api/office_hours/ticket.py`                                                                         | Handles main ticket-related API endpoints: creating, calling, closing, and canceling tickets.                                                                                          |
| `backend/api/office_hours/similar_tickets.py`                                                                | API endpoint to fetch similar past tickets using AI based on a current open ticket.                                                                                                    |
| `backend/entities/office_hours/ticket_entity.py`                                                             | Defines the database model (`OfficeHoursTicketEntity`) for office hour tickets in PostgreSQL.                                                                                          |
| `backend/services/office_hours/ticket.py`                                                                    | `OfficeHourTicketService` contains business logic for ticket lifecycle operations (create, call, close, cancel).                                                                       |
| `backend/services/office_hours/similar_tickets.py` and `backend/services/office_hours/similar_tickets_ai.py` | `OfficeHourSimilarTicketService` and `SimilarTicketAIService` manage AI interaction and ticket similarity logic.                                                                       |
| `backend/services/openai.py`                                                                                 | `OpenAIService` sends prompts to OpenAI and handles the LLM response for finding similar tickets.                                                                                      |
| **Models** (Pydantic)                                                                                        | `NewOfficeHoursTicket`, `OfficeHourTicketOverview`, `OfficeHoursTicketTAResponse`, `SimilarTicketsResponse`, and `SimilarTicketsAIResponse` define ticket structures and AI responses. |

### Frontend

| **File/Folder**                                                                | **Description**                                                                                                                                          |
| :----------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frontend/src/app/my-courses/course/office-hours/widgets/called-ticket-card/`  | Displays an open ticket after it’s called; provides a form for TAs to submit meeting summaries and solutions. Includes a **See Similar Tickets** button. |
| `frontend/src/app/my-courses/course/office-hours/widgets/ticket-summary-card/` | Displays a summarized view of a closed ticket, including TA notes and expandable student info.                                                           |
| `frontend/src/app/my-courses/course/office-hours/similar-tickets-page/`        | Page that shows similar past tickets retrieved via AI when TA clicks **See Similar Tickets**. Displays each result using `ticket-summary-card`.          |
| `frontend/src/app/my-courses/my-courses.service.ts`                            | Contains `callTicket`, `closeTicket`, and `seeSimilarTickets` methods that interact with backend APIs for ticket operations.                             |
| **Models**                                                                     | Uses shared `OfficeHourTicketOverview` and `OfficeHoursTicketTAResponse` models to handle ticket data on the frontend.                                   |
