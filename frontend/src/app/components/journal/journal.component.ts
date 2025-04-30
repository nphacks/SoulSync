import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-journal',
  templateUrl: './journal.component.html',
  styleUrl: './journal.component.scss'
})
export class JournalComponent {
  @Output() return = new EventEmitter<void>();

  returnToMain() {
    this.return.emit();
  }
}
