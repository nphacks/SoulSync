import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { JournalEntryService } from '../../services/journal-entry.service';

@Component({
  selector: 'app-text-journal',
  templateUrl: './text-journal.component.html',
  styleUrl: './text-journal.component.scss'
})
export class TextJournalComponent {
  journalEntry = new FormControl('');
  wordCount = 0;
  isSaving = false;
  
  constructor(private journalEntryService: JournalEntryService, private snackBar: MatSnackBar) {}

  updateWordCount() {
    const text = this.journalEntry.value || '';
    this.wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  }

  async submitEntry() {
    if (!this.journalEntry.value || this.wordCount > 300) return;
  
    this.isSaving = true;
    
    try {
      await this.journalEntryService.addTextEntry(this.journalEntry.value);
      this.snackBar.open('Journal entry saved successfully!', 'Close', { duration: 3000 });
      this.journalEntry.reset();
      this.wordCount = 0;
    } catch (error) {
      console.error('Error saving entry:', error);
      this.snackBar.open('Failed to save entry', 'Close', { duration: 3000 });
    } finally {
      this.isSaving = false;
    }
  }
}
