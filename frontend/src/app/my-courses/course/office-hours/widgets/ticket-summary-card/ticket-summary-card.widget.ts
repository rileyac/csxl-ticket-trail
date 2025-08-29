import {
  Component,
  EventEmitter,
  Input,
  Output,
  signal,
  WritableSignal
} from '@angular/core';
import { OfficeHourTicketOverview } from '../../../../my-courses.model';

@Component({
  selector: 'app-ticket-summary-card',
  // standalone: true,
  // imports: [],
  templateUrl: './ticket-summary-card.widget.html',
  styleUrl: './ticket-summary-card.widget.scss'
})
export class TicketSummaryCardWidget {
  @Input() ticket!: OfficeHourTicketOverview;
  expanded: WritableSignal<boolean> = signal(false);
  toggleExpanded() {
    console.log('Ticket type:', this.ticket.type); // should log 0

    this.expanded.set(!this.expanded());
  }
}
