/**
 * Office hours queue for instructors.
 *
 * @author Sarah Glenn
 * @copyright 2025
 */

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';
import { OfficeHourTicketOverview } from 'src/app/my-courses/my-courses.model';

@Component({
  selector: 'app-similar-tickets-page',
  templateUrl: './similar-tickets-page.component.html',
  styleUrl: './similar-tickets-page.component.css'
})
export class SimilarTicketsPageComponent implements OnInit {
  ticketId!: number;
  similarTickets: OfficeHourTicketOverview[] = [];
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private myCoursesService: MyCoursesService
  ) {}

  ngOnInit(): void {
    this.ticketId = Number(this.route.snapshot.paramMap.get('id'));

    this.myCoursesService.seeSimilarTickets(this.ticketId).subscribe({
      next: (tickets) => {
        console.log('Received tickets:', tickets);
        this.similarTickets = tickets.similar_tickets;
      },
      error: (err) => {
        this.error = 'Something went wrong';
        console.error(err);
      }
    });
  }
}
