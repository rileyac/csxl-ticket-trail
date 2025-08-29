"""Test Data for Office Hours."""

import pytest
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session

from backend.models.academics.my_courses import OfficeHourTicketOverview
from ...services.reset_table_id_seq import reset_table_id_seq

from ....test.services import user_data, room_data
from ..academics import section_data
from ..academics import term_data

from ....entities.office_hours import user_created_tickets_table
from ....entities.office_hours.office_hours_entity import OfficeHoursEntity
from ....entities.office_hours.course_site_entity import CourseSiteEntity
from ....entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from ....entities.academics.section_entity import SectionEntity
from ....entities.office_hours.office_hours_recurrence_pattern_entity import (
    OfficeHoursRecurrencePatternEntity,
)


from ....models.office_hours.office_hours_recurrence_pattern import (
    NewOfficeHoursRecurrencePattern,
    OfficeHoursRecurrencePattern,
)
from ....models.office_hours.office_hours import OfficeHours, NewOfficeHours
from ....models.office_hours.event_type import (
    OfficeHoursEventModeType,
    OfficeHoursEventType,
)
from ....models.office_hours.course_site import (
    CourseSite,
    NewCourseSite,
    UpdatedCourseSite,
)
from ....models.office_hours.ticket import OfficeHoursTicket, NewOfficeHoursTicket
from ....models.office_hours.ticket_type import TicketType
from ....models.office_hours.ticket_state import TicketState

__authors__ = [
    "Ajay Gandecha",
    "Madelyn Andrews",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

# Course Site Data

# COMP 110:

# Site
comp_110_site = CourseSite(id=1, title="COMP 110", term_id=term_data.current_term.id)
comp_301_site = CourseSite(id=2, title="COMP 301", term_id=term_data.current_term.id)

# Sections
comp_110_sections = (
    [
        section_data.comp_110_001_current_term,
        section_data.comp_110_002_current_term,
    ],
    comp_110_site.id,
)
comp_301_sections = (
    [section_data.comp_301_001_current_term],
    comp_301_site.id,
)


# Office Hours
comp_110_current_office_hours = OfficeHours(
    id=1,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Current CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() - timedelta(hours=2),
    end_time=datetime.now()
    + timedelta(weeks=4),  # changed this for month long OH, made week=4
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)
comp_110_future_office_hours = OfficeHours(
    id=2,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Future CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=1),
    end_time=datetime.now() + timedelta(days=1, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)
comp_110_past_office_hours = OfficeHours(
    id=3,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Past CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() - timedelta(days=1, hours=3),
    end_time=datetime.now() - timedelta(days=1),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)

# Recurring Office Hours
recurrence_pattern = OfficeHoursRecurrencePattern(
    id=1,
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=7),
    recur_monday=True,
    recur_tuesday=True,
    recur_wednesday=True,
    recur_thursday=True,
    recur_friday=True,
    recur_saturday=True,
    recur_sunday=True,
)
first_recurring_event = OfficeHours(
    id=4,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now(),
    end_time=datetime.now() + timedelta(hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
second_recurring_event = OfficeHours(
    id=5,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=1),
    end_time=datetime.now() + timedelta(days=1, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
third_recurring_event = OfficeHours(
    id=6,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=2),
    end_time=datetime.now() + timedelta(days=2, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
fourth_recurring_event = OfficeHours(
    id=7,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=3),
    end_time=datetime.now() + timedelta(days=3, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
fifth_recurring_event = OfficeHours(
    id=8,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=4),
    end_time=datetime.now() + timedelta(days=4, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
sixth_recurring_event = OfficeHours(
    id=9,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=5),
    end_time=datetime.now() + timedelta(days=5, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)
seventh_recurring_event = OfficeHours(
    id=10,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=6),
    end_time=datetime.now() + timedelta(days=6, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=1,
)

# Tickets
comp_110_queued_ticket_1 = OfficeHourTicketOverview(
    id=30,
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.QUEUED,
    created_at=datetime.now(),
    called_at=None,
    closed_at=None,
    assignment_section_description=None,
    meeting_summary=None,
    solutions_used=None,
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review=None,
    tactics_tried=None,
    concept_help_description="**Conceptual Question:  \nHow do you iterate through a nested for loop?**",
    code_to_english_description=None,
    concepts_needed_description=None,
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_queued_ticket_2 = OfficeHourTicketOverview(
    id=31,
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.QUEUED,
    created_at=datetime.now(),
    called_at=None,
    closed_at=None,
    assignment_section_description=None,
    meeting_summary=None,
    solutions_used=None,
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review=None,
    tactics_tried=None,
    concept_help_description="**Conceptual Question**:  \nWhat is the difference between a list and a tuple in Python?",
    code_to_english_description=None,
    concepts_needed_description=None,
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_queued_ticket_3 = OfficeHourTicketOverview(
    id=32,
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.QUEUED,
    created_at=datetime.now(),
    called_at=None,
    closed_at=None,
    assignment_section_description=None,
    meeting_summary=None,
    solutions_used=None,
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review=None,
    tactics_tried=None,
    concept_help_description="**Conceptual Question**:  \nHow do if-else statements work to control the flow of a program?",
    code_to_english_description=None,
    concepts_needed_description=None,
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)


comp_110_cancelled_ticket = OfficeHourTicketOverview(
    id=40,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CANCELED,
    created_at=datetime.now(),
    called_at=None,
    closed_at=None,
    assignment_section_description="**Assignment Part**:  \nI'm trying to iterate through a list of students and print each one.",
    meeting_summary=None,
    solutions_used=None,
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review=None,
    tactics_tried="**Tried**:  \nchecked class notes, asked peer",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nPrint every item in a list of numbers",
    concepts_needed_description="**Concepts**:  \nHow to access each item in a list using a for loop",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)
comp_110_called_ticket = OfficeHourTicketOverview(
    id=50,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CALLED,
    created_at=datetime.now() - timedelta(minutes=1),
    called_at=datetime.now(),
    closed_at=None,
    assignment_section_description="**Assignment Part**:  \nI'm trying to loop through a list of grades and print each one.",
    meeting_summary=None,
    solutions_used=None,
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review=None,
    tactics_tried="**Tried**:  \nchecked class notes, asked peer",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nPrint every item in a list of numbers",
    concepts_needed_description="**Concepts**:  \nhow to access each item in a list using a for loop",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)
comp_110_closed_ticket_1 = OfficeHourTicketOverview(
    id=1,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=45),
    called_at=datetime.now() - timedelta(minutes=43),
    assignment_section_description="**Assignment Part**:  \nI'm trying to loop through a list of grades and print each one.",
    meeting_summary="Student had incorrect indentation and was modifying the list while iterating. We rewrote the loop to cleanly print each grade.",
    solutions_used="Walked through a list example and discussed what happens when you modify a list while looping.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="basic for loop over list",
    tactics_tried="**Tried**:  \nchecked class notes, asked peer",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nPrint every item in a list of numbers",
    concepts_needed_description="**Concepts**:  \nhow to access each item in a list using a for loop",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_2 = OfficeHourTicketOverview(
    id=2,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=50),
    called_at=datetime.now() - timedelta(minutes=47),
    assignment_section_description="**Assignment Part**:  \nTrying to print a message with both the item and its index.",
    meeting_summary="Showed how to use `range(len(my_list))` and access both index and value using indexing.",
    solutions_used="Demonstrated with a list of fruits, used print statements to visualize index-value pairs, and explained what len() returns.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="range and list indexing",
    tactics_tried="**Tried**:  \ntried looping with 'for item in list'",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nPrint: 'Index 0 is apple', etc.",
    concepts_needed_description="**Concepts**:  \nhow to print index and value from a list using a for loop",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_3 = OfficeHourTicketOverview(
    id=3,
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=60),
    called_at=datetime.now() - timedelta(minutes=56),
    concept_help_description="**Conceptual Question**:  \n I don't understand what the range function does in a for loop.",
    meeting_summary="Explained what `range()` returns and how it’s used to repeat code a set number of times.",
    solutions_used="Wrote a for loop that used range() with print statements and compared examples using different start/stop/step inputs.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="range(), for loop iteration",
    tactics_tried=None,
    assignment_section_description=None,
    code_to_english_description=None,
    concepts_needed_description=None,
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_4 = OfficeHourTicketOverview(
    id=4,
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=68),
    called_at=datetime.now() - timedelta(minutes=65),
    concept_help_description="**Conceptual Question**:  \nI used 'i' in a for loop, and now I’m confused why I can’t use it outside the loop afterward.",
    meeting_summary="Explained how loop variables like 'i' are often limited in scope, depending on context. Showed what happens when you try to access them outside the loop in Python.",
    solutions_used="Walked through a code example where 'i' is defined in a for loop and then referenced after. Discussed Python’s handling of loop variables and demonstrated why this can lead to confusing behavior or errors in some languages.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="loop variable scope, for loop behavior",
    tactics_tried=None,
    assignment_section_description=None,
    code_to_english_description=None,
    concepts_needed_description=None,
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)


comp_110_closed_ticket_5 = OfficeHourTicketOverview(
    id=5,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=75),
    called_at=datetime.now() - timedelta(minutes=72),
    assignment_section_description="**Assignment Part**:  \nTrying to write a loop that prints every other item in a list.",
    meeting_summary="Student wasn’t sure how to skip items using `range`. Showed them how to use a step of 2.",
    solutions_used="Illustrated range(0, len(list), 2) with a written index table, and explained stepping over values",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="range() step argument, for loops",
    tactics_tried="**Tried**:  \nre-watching lecture, trying random numbers in range()",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nPrint items at index 0, 2, 4, etc.",
    concepts_needed_description="**Concepts**:  \nhow to loop over every other item, maybe using a for loop",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)
comp_110_closed_ticket_6 = OfficeHourTicketOverview(
    id=6,
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=80),
    called_at=datetime.now() - timedelta(minutes=77),
    concept_help_description="**Conceptual Question**:  \nWhy do we use def to create a function, and where does the code go?",
    meeting_summary="Student was unclear about the structure of a function. We walked through defining one and calling it from main.",
    solutions_used="Used a cooking analogy to explain function definitions as recipes, showed indentation rules, and explained how to call the function from inside another block.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="function definitions, code blocks",
    tactics_tried=None,
    assignment_section_description=None,
    code_to_english_description=None,
    concepts_needed_description=None,
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_7 = OfficeHourTicketOverview(
    id=7,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=85),
    called_at=datetime.now() - timedelta(minutes=81),
    assignment_section_description="**Assignment Part**:  \nTrying to define a function that greets a user by name, but I keep getting errors about arguments.",
    meeting_summary="Student forgot to include a parameter in the function definition. We matched the number of parameters to arguments in the function call.",
    solutions_used="Explained difference between parameters and arguments, drew a diagram of a function box that takes inputs, and corrected the call to include a string.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="parameters vs arguments",
    tactics_tried="**Tried**:  \ntrial and error",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nDefine a function that prints Hello to a name you give it",
    concepts_needed_description="**Concepts**:  \nhow to pass info into a function",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_8 = OfficeHourTicketOverview(
    id=8,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=90),
    called_at=datetime.now() - timedelta(minutes=87),
    assignment_section_description="**Assignment Part**:  \nI'm defining a function that returns True if a number is even, but it keeps printing None.",
    meeting_summary="Student was printing inside the function instead of using return. We rewrote it with a return statement.",
    solutions_used="Compared a return vs print example side by side, explained why returning is needed for conditional checks, and traced what the calling line receives.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="return vs print for functions",
    tactics_tried="**Tried**:  \nwatched function lecture again",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nCreate a function that returns True if a number is divisible by 2",
    concepts_needed_description="**Concepts**:  \nhow to return values instead of printing",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_9 = OfficeHourTicketOverview(
    id=9,
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=95),
    called_at=datetime.now() - timedelta(minutes=92),
    concept_help_description="**Conceptual Question**:  \nWhat happens if I define a function after I try to use it?",
    meeting_summary="Student called a function before it was defined. We talked through Python’s top-down reading of code.",
    solutions_used="Moved the function above main, showed error message that mentions undefined name, and explained interpreter behavior step-by-step.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="function call order, top-down execution",
    tactics_tried=None,
    assignment_section_description=None,
    code_to_english_description=None,
    concepts_needed_description=None,
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_10 = OfficeHourTicketOverview(
    id=10,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=100),
    called_at=datetime.now() - timedelta(minutes=97),
    assignment_section_description="**Assignment Part**:  \nTrying to reuse a helper function from a previous problem, but not sure how to organize my code.",
    meeting_summary="Student copied the function into the wrong scope and was confused about how to import from another file. We rewrote it in the right place.",
    solutions_used="Clarified scope vs reuse for functions and walked through file structure.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="reusing functions, organizing code",
    tactics_tried="**Tried**:  \ncopy/paste and trying to call from current file",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nCall a previously defined function to simplify new code",
    concepts_needed_description="**Concepts**:  \nhow to reuse helper functions",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_11 = OfficeHourTicketOverview(
    id=11,
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=110),
    called_at=datetime.now() - timedelta(minutes=107),
    concept_help_description="**Conceptual Question**:  \nI don't understand what a base case is in recursion.",
    meeting_summary="Explained that a base case is what stops the recursion and prevents it from running forever. We wrote a simple factorial function with a base case of 1.",
    solutions_used="Used factorial as an example, wrote out a recursive trace on paper, and showed how the base case limits the recursive calls.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="base case in recursion",
    tactics_tried=None,
    assignment_section_description=None,
    code_to_english_description=None,
    concepts_needed_description=None,
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_12 = OfficeHourTicketOverview(
    id=12,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=115),
    called_at=datetime.now() - timedelta(minutes=112),
    assignment_section_description="**Assignment Part**:  \nMy recursive function seems to be running forever and never returning anything.",
    meeting_summary="Student's base case condition was incorrect, causing infinite recursion. We added print statements to visualize the recursive calls.",
    solutions_used="Wrote out the recursive calls on paper, used print statements to show function parameters as they changed, and corrected the base case condition.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="base case, stopping recursion",
    tactics_tried="**Tried**:  \ndebugging with print statements",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nA recursive function to calculate factorial, including a base case to stop recursion.",
    concepts_needed_description="**Concepts**:  \nhow to prevent infinite recursion with a base case",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_13 = OfficeHourTicketOverview(
    id=13,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=120),
    called_at=datetime.now() - timedelta(minutes=117),
    assignment_section_description="**Assignment Part**:  \nTrying to sum a list recursively, but I'm not sure how to reduce the list in each recursive call.",
    meeting_summary="Student was trying to pass the entire list each time, instead of reducing it by removing the first element in each recursive call.",
    solutions_used="Explained how to reduce the list by slicing (my_list[1:]) in each recursive call, and worked through the logic together.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="recursive list reduction",
    tactics_tried="**Tried**:  \nsearched online, copied sample code",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nSum the numbers in a list recursively by reducing the list each time.",
    concepts_needed_description="**Concepts**:  \nhow to reduce a problem in each recursive call",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_14 = OfficeHourTicketOverview(
    id=14,
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=125),
    called_at=datetime.now() - timedelta(minutes=122),
    concept_help_description="**Conceptual Question**:  \nWhat happens when a recursive function calls itself?",
    meeting_summary="Explained the call stack and how each recursive call creates a new stack frame. Discussed how the function eventually resolves once the base case is reached.",
    solutions_used="Used a diagram to show the recursive call stack, and broke down the process step by step.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="recursive call stack, function resolution",
    tactics_tried=None,
    assignment_section_description=None,
    code_to_english_description=None,
    concepts_needed_description=None,
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_15 = OfficeHourTicketOverview(
    id=15,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=130),
    called_at=datetime.now() - timedelta(minutes=127),
    assignment_section_description="**Assignment Part**:  \nI'm trying to calculate Fibonacci numbers recursively, but it’s too slow. Can I optimize this?",
    meeting_summary="Student’s Fibonacci function was recalculating the same values multiple times. We discussed using memoization to store already calculated values.",
    solutions_used="Explained how to store results in a dictionary and check for existing values before recalculating. Walked through both recursive and memoized versions.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="memoization in recursion",
    tactics_tried="**Tried**:  \nrefactored code, searched for better methods",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nRecursive Fibonacci with memoization for faster calculation.",
    concepts_needed_description="**Concepts**:  \nhow to optimize recursive functions with memoization",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)


comp_110_closed_ticket_RB1 = OfficeHourTicketOverview(
    id=16,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=135),
    called_at=datetime.now() - timedelta(minutes=132),
    assignment_section_description="**Assignment Part**:  \nI'm trying to implement insertions into a red-black tree but my tree doesn't stay balanced.",
    meeting_summary="Student was missing the necessary rotations after inserting. We reviewed when to perform left and right rotations based on uncle colors.",
    solutions_used="Walked through the red-black tree insertion cases (uncle red vs black) with diagrams. Stepped through example inserts manually.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="red-black tree rotations, insertion cases",
    tactics_tried="**Tried**:  \nreading lecture notes, inserting test values",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nInsert values into a red-black tree while preserving all properties.",
    concepts_needed_description="**Concepts**:  \nhow and when to rotate nodes after insertion",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_RB2 = OfficeHourTicketOverview(
    id=17,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=140),
    called_at=datetime.now() - timedelta(minutes=137),
    assignment_section_description="**Assignment Part**:  \nI'm confused about how recoloring works when adding a node to a red-black tree.",
    meeting_summary="Student didn’t understand when to recolor vs rotate. We broke down the color rules after insertions, focusing on parent, uncle, and grandparent relationships.",
    solutions_used="Reviewed the red-black properties, especially about red parents. Used sample insertions to show when recoloring is sufficient without rotating.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="red-black tree recoloring",
    tactics_tried="**Tried**:  \ntraced some examples but got stuck",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nUnderstand recoloring logic during insertion.",
    concepts_needed_description="**Concepts**:  \nred-black tree recoloring rules",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_RB3 = OfficeHourTicketOverview(
    id=18,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=145),
    called_at=datetime.now() - timedelta(minutes=142),
    assignment_section_description="**Assignment Part**:  \nI'm trying to delete a node from my red-black tree but it’s breaking the tree properties.",
    meeting_summary="Student was not handling the double black cases properly after deletion. We reviewed the different cases for fixing double black nodes after removal.",
    solutions_used="Went over red-black tree deletion cases, including when to rotate, recolor, or move the problem up the tree.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="red-black tree deletion cases",
    tactics_tried="**Tried**:  \nfollowing pseudocode from class, modifying parent pointers",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nDelete nodes from a red-black tree correctly.",
    concepts_needed_description="**Concepts**:  \nhandling double black situations after deletion",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_RB4 = OfficeHourTicketOverview(
    id=19,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=150),
    called_at=datetime.now() - timedelta(minutes=147),
    assignment_section_description="**Assignment Part**:  \nI'm confused about how the root node should be treated in a red-black tree after insertions and deletions.",
    meeting_summary="Student didn’t realize the root must always be black after any insertion or deletion. We explained how root recoloring can fix violations.",
    solutions_used="Drew tree diagrams and discussed fixing up to the root. Practiced ensuring root blackness after rebalancing.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="red-black tree root rules",
    tactics_tried="**Tried**:  \nchecking code comments but unsure",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nMake sure the root of a red-black tree is always black.",
    concepts_needed_description="**Concepts**:  \npost-insertion and deletion fixes for root",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_RB5 = OfficeHourTicketOverview(
    id=20,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=155),
    called_at=datetime.now() - timedelta(minutes=152),
    assignment_section_description="**Assignment Part**:  \nMy red-black tree implementation passes small tests but fails big ones. How can I debug tree properties?",
    meeting_summary="Student didn’t have good debug tools. We walked through adding helper functions to check black heights, node colors, and path properties after every operation.",
    solutions_used="Helped student write helper methods to validate red-black properties programmatically after inserts/deletes.",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review="validating tree properties",
    tactics_tried="**Tried**:  \nmanual checking, small examples",
    concept_help_description=None,
    code_to_english_description="**Goal**:  \nDebug a red-black tree using validation methods.",
    concepts_needed_description="**Concepts**:  \nautomated red-black property checking",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)

comp_110_closed_ticket_unrelated = OfficeHourTicketOverview(
    id=21,
    type=TicketType.CONCEPTUAL_HELP,
    state=TicketState.CLOSED,
    created_at=datetime.now() - timedelta(minutes=155),
    called_at=datetime.now() - timedelta(minutes=152),
    assignment_section_description=None,
    meeting_summary="Went over common chemical reactions",
    solutions_used="Organic chemistry tutor",
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review=None,
    tactics_tried=None,
    concept_help_description="Organic chemistry",
    code_to_english_description=None,
    concepts_needed_description=None,
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)


##AI testing tickets

red_black_called_ticket = OfficeHourTicketOverview(
    id=51,
    type=TicketType.ASSIGNMENT_HELP,
    state=TicketState.CALLED,
    created_at=datetime.now() - timedelta(minutes=1),
    called_at=datetime.now(),
    closed_at=None,
    assignment_section_description="**Assignment Part**: \nWorking on balancing a red-black tree after insertions.",
    meeting_summary=None,
    solutions_used=None,
    office_hours_id=comp_110_current_office_hours.id,
    concepts_for_review=None,
    tactics_tried="**Tried**: inserting nodes without balancing",
    concept_help_description=None,
    code_to_english_description="**Goal**: \nEnsure tree stays balanced after adding new nodes",
    concepts_needed_description="**Concepts**:  \nrotations and color flips in red-black trees",
    caller=None,
    caller_id=section_data.comp110_instructor.id,
)


comp_110_ticket_creators = [
    (comp_110_queued_ticket_1, [section_data.comp110_student_1.id]),
    (comp_110_queued_ticket_2, [section_data.comp110_student_1.id]),
    (comp_110_queued_ticket_3, [section_data.comp110_student_1.id]),
    (comp_110_cancelled_ticket, [section_data.comp110_student_1.id]),
    (comp_110_called_ticket, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_1, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_2, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_3, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_4, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_5, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_6, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_7, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_8, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_9, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_10, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_11, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_12, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_13, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_14, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_15, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_RB1, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_RB2, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_RB3, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_RB4, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_RB5, [section_data.comp110_student_1.id]),
    (red_black_called_ticket, [section_data.comp110_student_1.id]),
    (comp_110_closed_ticket_unrelated, [section_data.comp110_student_1.id]),
]

# All
sites = [comp_110_site, comp_301_site]
section_pairings = [comp_110_sections, comp_301_sections]

recurrence_patterns = [recurrence_pattern]

office_hours = [
    comp_110_current_office_hours,
    comp_110_future_office_hours,
    comp_110_past_office_hours,
    first_recurring_event,
    second_recurring_event,
    third_recurring_event,
    fourth_recurring_event,
    fifth_recurring_event,
    sixth_recurring_event,
    seventh_recurring_event,
]

oh_tickets = [
    comp_110_queued_ticket_1,
    comp_110_queued_ticket_2,
    comp_110_queued_ticket_3,
    comp_110_cancelled_ticket,
    comp_110_called_ticket,
    comp_110_closed_ticket_1,
    comp_110_closed_ticket_2,
    comp_110_closed_ticket_3,
    comp_110_closed_ticket_4,
    comp_110_closed_ticket_5,
    comp_110_closed_ticket_6,
    comp_110_closed_ticket_7,
    comp_110_closed_ticket_8,
    comp_110_closed_ticket_9,
    comp_110_closed_ticket_10,
    comp_110_closed_ticket_11,
    comp_110_closed_ticket_12,
    comp_110_closed_ticket_13,
    comp_110_closed_ticket_14,
    comp_110_closed_ticket_15,
    comp_110_closed_ticket_RB1,
    comp_110_closed_ticket_RB2,
    comp_110_closed_ticket_RB3,
    comp_110_closed_ticket_RB4,
    comp_110_closed_ticket_RB5,
    red_black_called_ticket,
    comp_110_closed_ticket_unrelated,
]
ticket_user_pairings = [comp_110_ticket_creators]


def insert_fake_data(session: Session):

    # Step 1: Add sites to database

    for site in sites:
        entity = CourseSiteEntity.from_model(site)
        session.add(entity)

    reset_table_id_seq(
        session,
        CourseSiteEntity,
        CourseSiteEntity.id,
        len(sites) + 1,
    )

    session.commit()

    # Step 2: Add sections to course sites
    for sections, site_id in section_pairings:
        for section in sections:
            section_entity = session.get(SectionEntity, section.id)
            section_entity.course_site_id = site_id

    session.commit()

    # Step 3: Add office hours to database
    for oh in office_hours:
        office_hours_entity = OfficeHoursEntity.from_model(oh)
        session.add(office_hours_entity)

    reset_table_id_seq(
        session,
        OfficeHoursEntity,
        OfficeHoursEntity.id,
        len(office_hours) + 1,
    )

    session.commit()

    for pattern in recurrence_patterns:
        recurrence_pattern_entity = OfficeHoursRecurrencePatternEntity.from_model(
            pattern
        )
        session.add(recurrence_pattern_entity)

    reset_table_id_seq(
        session,
        OfficeHoursRecurrencePatternEntity,
        OfficeHoursRecurrencePatternEntity.id,
        len(recurrence_patterns) + 1,
    )

    session.commit()

    # Step 4: Add tickets to database

    for ticket in oh_tickets:
        ticket_entity = OfficeHoursTicketEntity.from_overview_model(ticket)
        session.add(ticket_entity)

    reset_table_id_seq(
        session,
        OfficeHoursTicketEntity,
        OfficeHoursTicketEntity.id,
        len(oh_tickets) + 1,
    )

    session.commit()

    # Step 5: Add users as ticket creators
    for pairing in ticket_user_pairings:
        for ticket, user_ids in pairing:
            for user_id in user_ids:
                session.execute(
                    user_created_tickets_table.insert().values(
                        {
                            "ticket_id": ticket.id,
                            "member_id": user_id,
                        }
                    )
                )

    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield


# Data objects for testing purposes

new_ticket = NewOfficeHoursTicket(
    description="Help me!",
    type=TicketType.ASSIGNMENT_HELP,
    office_hours_id=comp_110_current_office_hours.id,
)

new_course_site = NewCourseSite(
    title="Ina's COMP 301",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_301_002_current_term.id,
    ],
)

new_course_site_term_mismatch = NewCourseSite(
    title="Ina's COMP 301",
    term_id=term_data.f_23.id,
    section_ids=[
        section_data.comp_301_002_current_term.id,
    ],
)


new_course_site_term_nonmember = NewCourseSite(
    title="Ina's COMP 3x1",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_301_002_current_term.id,
        section_data.comp_311_001_current_term.id,
    ],
)
new_course_site_term_noninstructor = NewCourseSite(
    title="Ina's COMP 3x1",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_301_002_current_term.id,
        section_data.comp_311_002_current_term.id,
    ],
)


new_course_site_term_already_in_site = NewCourseSite(
    title="Ina's COMP courses",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_301_002_current_term.id,
        section_data.comp_110_001_current_term.id,
    ],
)

updated_comp_110_site = UpdatedCourseSite(
    id=1,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[section_data.comp_110_001_current_term.id],
    utas=[],
    gtas=[],
)

updated_comp_110_site_term_mismatch = UpdatedCourseSite(
    id=1,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_110_001_current_term.id,
        section_data.comp_101_001.id,
    ],
    utas=[],
    gtas=[],
)

updated_course_site_term_nonmember = UpdatedCourseSite(
    id=1,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_110_001_current_term.id,
        section_data.comp_311_001_current_term.id,
    ],
    utas=[],
    gtas=[],
)

updated_course_does_not_exist = UpdatedCourseSite(
    id=404,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_110_001_current_term.id,
        section_data.comp_311_002_current_term.id,
    ],
    utas=[],
    gtas=[],
)

updated_course_site_term_noninstructor = UpdatedCourseSite(
    id=1,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_311_001_current_term.id,
        section_data.comp_311_002_current_term.id,
    ],
    utas=[],
    gtas=[],
)

updated_course_site_term_already_in_site = UpdatedCourseSite(
    id=1,
    title="New Course Site",
    term_id=term_data.current_term.id,
    section_ids=[
        section_data.comp_301_001_current_term.id,
        section_data.comp_110_001_current_term.id,
    ],
    utas=[],
    gtas=[],
)

new_site_other_user = NewCourseSite(
    title="Rhonda",
    term_id=term_data.current_term.id,
    section_ids=[section_data.comp_311_001_current_term.id],
)

new_event = NewOfficeHours(
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Sample",
    location_description="Sample",
    start_time=datetime.now(),
    end_time=datetime.now() + timedelta(hours=1),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)

new_recurrence_pattern = NewOfficeHoursRecurrencePattern(
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=14),
    recur_monday=True,
    recur_tuesday=True,
    recur_wednesday=True,
    recur_thursday=True,
    recur_friday=True,
    recur_saturday=True,
    recur_sunday=True,
)

updated_recurrence_pattern = NewOfficeHoursRecurrencePattern(
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=14),
    recur_monday=True,
    recur_tuesday=False,
    recur_wednesday=True,
    recur_thursday=False,
    recur_friday=True,
    recur_saturday=True,
    recur_sunday=True,
)

invalid_recurrence_pattern_days = NewOfficeHoursRecurrencePattern(
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=14),
    recur_monday=False,
    recur_tuesday=False,
    recur_wednesday=False,
    recur_thursday=False,
    recur_friday=False,
    recur_saturday=False,
    recur_sunday=False,
)

invalid_recurrence_pattern_end = NewOfficeHoursRecurrencePattern(
    start_date=datetime.now() - timedelta(days=14),
    end_date=datetime.now() - timedelta(days=13),
    recur_monday=True,
    recur_tuesday=False,
    recur_wednesday=False,
    recur_thursday=False,
    recur_friday=False,
    recur_saturday=False,
    recur_sunday=False,
)

new_event_site_not_found = NewOfficeHours(
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Sample",
    location_description="Sample",
    start_time=datetime.now(),
    end_time=datetime.now() + timedelta(hours=1),
    course_site_id=404,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)

updated_future_event = OfficeHours(
    id=2,
    type=OfficeHoursEventType.REVIEW_SESSION,
    mode=OfficeHoursEventModeType.VIRTUAL_OUR_LINK,
    description="Future CAMP 110 office hours",
    location_description="In the downstairs closet : )",
    start_time=datetime.now() + timedelta(days=1),
    end_time=datetime.now() + timedelta(days=1, hours=3),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)

nonexistent_event = OfficeHours(
    id=404,
    type=OfficeHoursEventType.OFFICE_HOURS,
    mode=OfficeHoursEventModeType.IN_PERSON,
    description="Sample",
    location_description="Sample",
    start_time=datetime.now(),
    end_time=datetime.now() + timedelta(hours=1),
    course_site_id=comp_110_site.id,
    room_id=room_data.group_a.id,
    recurrence_pattern_id=None,
)
