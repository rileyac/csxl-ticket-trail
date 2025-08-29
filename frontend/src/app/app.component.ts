import { Component, OnInit } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { Observable, filter } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {
  title = 'frontend';
  childRoute: string = '';

  constructor(
    private matIconReg: MatIconRegistry,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.matIconReg.setDefaultFontSetClass('material-symbols-outlined');

    this.router.events
      .pipe(filter((event) => event instanceof NavigationEnd))
      .subscribe(() => {
        const firstChild = this.route.firstChild;
        if (firstChild && firstChild.snapshot.url.length) {
          // checks for expected case where the childRoute isn't empty
          this.childRoute = firstChild.snapshot.url[0].path;
        } else {
          // helps navigation in case of my-courses where the route was an empty path ('')
          this.childRoute = 'root'; // fallback label
        }
      });

    // this.router.events
    //   .pipe(filter((event) => event instanceof NavigationEnd))
    //   .subscribe(() => {
    //     // When the route navigation is completed, get the child
    //     this.childRoute =
    //       this.route.firstChild?.snapshot.url[0].path || 'root';
    //   });
  }
}
