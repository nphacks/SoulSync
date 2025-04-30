import { Component } from '@angular/core';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'SoulSync';
  showProfileView = false;
  showJournalView = false;

  constructor(public authService: AuthService) {}

  showProfile() {
    this.showProfileView = true;
    this.showJournalView = false;
  }

  showJournal() {
    this.showJournalView = true;
    this.showProfileView = false;
  }

  // Call this when you want to return to main view
  returnToMain() {
    this.showProfileView = false;
    this.showJournalView = false;
  }
}
