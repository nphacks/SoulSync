import { Component, EventEmitter, OnInit, Output, signal, ChangeDetectionStrategy } from '@angular/core';
import { JournalEntryService } from '../../services/journal-entry.service';
import { ChangeDetectorRef } from '@angular/core';


@Component({
  selector: 'app-journal',
  templateUrl: './journal.component.html',
  styleUrl: './journal.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class JournalComponent implements OnInit {
  @Output() return = new EventEmitter<void>();
  entries: any;
  loading = true;
  userId: string = '';
  debug = true; 
  error: string | null = null;
  readonly panelOpenState = signal(false);

  constructor(
    private journalService: JournalEntryService,
    private cd: ChangeDetectorRef
  ) {}

  ngOnInit() {
    console.log('Component initialized');
    this.loadEntries();
  }

  async loadEntries() {
    try {
      const userData = JSON.parse(localStorage.getItem('userData') || '{}');
      const userId = userData.user_id;

      this.journalService.getEntries(userId).subscribe({
        next: (data) => {
          console.log('Received data:', data);
          this.entries = data;
          this.loading = false;
          this.error = null;
          this.cd.detectChanges();
        },
        error: (err) => {
          console.error('Error:', err);
          this.error = 'Failed to load entries';
          this.loading = false;
          this.entries = { entries: [] }; // Ensure empty state
        }
      });
    } catch (err) {
      console.error('Initialization error:', err);
      this.error = 'Initialization failed';
      this.loading = false;
    }
  }

  getSentimentClass(sentiment: string): string {
    switch(sentiment?.toLowerCase()) {
      case 'positive': return 'positive';
      case 'negative': return 'negative';
      case 'neutral': return 'neutral';
      default: return '';
    }
  }

  getAudioUrl(blobData: any): string {
    // Convert blob data to playable URL
    return URL.createObjectURL(new Blob([blobData], { type: 'audio/mpeg' }));
  }

  parseChatbotData(chatData: string): any[] {
    try {
      return JSON.parse(chatData);
    } catch (e) {
      return [
        { role: 'system', content: 'Could not parse conversation data' },
        { role: 'error', content: chatData }
      ];
    }
  }

  parseTimestamp(timestamp: any): Date {
    // 1. Handle MongoDB-style format
    if (timestamp?.$date) {
      return new Date(timestamp.$date);
    }
    
    // 2. If it's already a Date object
    if (timestamp instanceof Date) return timestamp;
    
    // 3. If it's a string/number
    if (typeof timestamp === 'string' || typeof timestamp === 'number') {
      return new Date(timestamp);
    }
    
    // 4. If it's an object with seconds/nanos (Firestore format)
    if (timestamp?.seconds) {
      return new Date(timestamp.seconds * 1000);
    }
    
    console.warn('Unrecognized timestamp format:', timestamp);
    return new Date(); // Fallback (only if format is unrecognized)
  }

  // Add this to your component
  formatDate(timestamp: any): string {
    try {
      const date = this.parseTimestamp(timestamp);
      return date.toLocaleString(); // Or any other format
    } catch (e) {
      return 'Unknown date';
    }
  }

  returnToMain() {
    this.return.emit();
  }
}
