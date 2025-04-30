import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  unreadCount = 0; 

  @Output() profileClicked = new EventEmitter<void>();
  @Output() journalClicked = new EventEmitter<void>();

  onProfileClick() {
    this.profileClicked.emit();
  }

  onJournalClick() {
    this.journalClicked.emit();
  }
}
