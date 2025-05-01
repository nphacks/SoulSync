import { Component, EventEmitter, Output } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  unreadCount = 0; 

  constructor(private authService: AuthService) {}

  @Output() profileClicked = new EventEmitter<void>();
  @Output() journalClicked = new EventEmitter<void>();

  onProfileClick() {
    this.profileClicked.emit();
  }

  onJournalClick() {
    this.journalClicked.emit();
  }

  logout() {
    this.authService.logout()
  }
}
