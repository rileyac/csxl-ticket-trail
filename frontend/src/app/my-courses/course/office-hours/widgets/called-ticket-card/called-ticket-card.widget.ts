/**
 * The Called Ticket Card widget defines the UI card for
 * a called ticket in an OH queue.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges,
  WritableSignal,
  signal
} from '@angular/core';
import {
  OfficeHourGetHelpOverview,
  OfficeHourTicketOverview,
  OfficeHourTicketTAResponse,
  TicketDraft
} from '../../../../my-courses.model';
import {
  FormControl,
  Validators,
  FormBuilder,
  FormGroup
} from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';
import { Router } from '@angular/router';

@Component({
  selector: 'called-ticket-card',
  templateUrl: './called-ticket-card.widget.html',
  styleUrls: ['./called-ticket-card.widget.scss']
})
export class CalledTicketCardWidget implements OnChanges {
  @Input() ticket!: OfficeHourTicketOverview;
  @Input() calledByUser: boolean = false;
  @Output() closeButtonPressed = new EventEmitter<OfficeHourTicketOverview>(); //this is sending an officehourticketoverview object, but shouldnt it be a completed officehourticket object?
  @Output() similarTicketButtonPressed = new EventEmitter<Number>();

  expanded: WritableSignal<boolean> = signal(false);

  public taResponseForm = this.formBuilder.group({
    meetingSummary: new FormControl('', [Validators.required]),
    toolsUsed: new FormControl('', [Validators.required]),
    conceptsForReview: new FormControl('') //why is this not required input?
  });

  constructor(
    private formBuilder: FormBuilder,
    private http: HttpClient,
    protected myCoursesService: MyCoursesService,
    private router: Router
  ) {}

  toggleExpanded() {
    this.expanded.set(!this.expanded());
  }

  closeButtonEvent() {
    if (this.taResponseForm.controls['meetingSummary'].value) {
      console.log('meeting summary set', this.ticket.id);
      this.ticket.meeting_summary =
        this.taResponseForm.controls['meetingSummary'].value;
    }

    if (this.taResponseForm.controls['toolsUsed'].value) {
      this.ticket.solutions_used =
        this.taResponseForm.controls['toolsUsed'].value;
    }

    if (this.taResponseForm.controls['conceptsForReview'].value) {
      this.ticket.concepts_for_review =
        this.taResponseForm.controls['conceptsForReview'].value;
    }

    // if (this.ticket.meeting_summary == '' || this.ticket.solutions_used == ''){

    // }

    const TAresponse: OfficeHourTicketTAResponse = {
      meeting_summary: this.ticket.meeting_summary,
      solutions_used: this.ticket.solutions_used,
      concepts_for_review: this.ticket.concepts_for_review
    };

    console.log('close ticket called', this.ticket.id);
    this.myCoursesService.closeTicket(this.ticket.id, TAresponse).subscribe({
      next: (response) => {
        console.log('Ticket closed successfully:', response);
        // this.closeButtonPressed.emit(this.ticket);
        this.closeButtonPressed.emit(response);
      },
      error: (err) => {
        console.error('Error closing ticket:', err);
      }
    }); // subscribe?
    //next:
  }

  // similarTicketButtonEvent() {
  //   this.myCoursesService.seeSimilarTickets(this.ticket.id).subscribe({
  //     next: (response) => {
  //       console.log('See similar tickets:', response);
  //       this.similarTicketButtonPressed.emit();
  //     },
  //     error: (err) => {
  //       console.error('Error getting similar tickets:', err);
  //     }
  //   }); // subscribe?
  // }

  // Maybe modify to open in new tab??
  similarTicketButtonEvent() {
    console.log('Button clicked');
    this.router.navigateByUrl(`office-hours/ticket/${this.ticket.id}/similar`);
  }

  ngOnChanges(changes: SimpleChanges): void {
    // If the TA calling the ticket is the active user, expand the card
    if (changes['calledByUser'] && changes['calledByUser'].currentValue) {
      this.expanded.set(true);
    }
  }
  //dont know if this is needed

  data: WritableSignal<OfficeHourGetHelpOverview | undefined> =
    signal(undefined);

  // submitTicketForm() {
  // //TODO: figure this out
  // }
}
