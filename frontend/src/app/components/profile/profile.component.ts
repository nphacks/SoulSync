import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss'
})
export class ProfileComponent implements OnInit {
  @Output() return = new EventEmitter<void>();

  user: any;
  loading = true;
  originalSettings: any;
  settings: any = {
    therapist: { name: '', email: '' },
    sentimentShare: false,
    emotionShare: false,
    topicShare: false,
    summaryShare: false,
    extremeEmotions: false
  };
  hasChanges = false;
  selectedReport: string = 'activity'; // Default selection

  constructor(private authService: AuthService) {}

  ngOnInit() {
    // this.loadUserSettings();
  }

  loadUserSettings() {
    this.authService.getUserInformation().subscribe({
      next: (data) => {
        if (data) {
          this.settings = {
            therapist: {
              name: data.therapist?.name || '',  // Fallback to empty string if undefined
              email: data.therapist?.email || ''
            },
            sentimentShare: data.sentimentShare || false,
            emotionShare: data.emotionShare || false,
            topicShare: data.topicShare || false,
            summaryShare: data.summaryShare || false,
            extremeEmotions: data.extremeEmotions || false,
          };
        }
      },
      error: (err) => console.error('Error loading settings:', err)
    });
  }

  onToggleChange(field: string) {
    console.log(`${field} changed to:`, this.settings[field]);
  }
  
  saveSettings() {
    // Implement your save logic here
    console.log('Saving settings:', this.settings);
    // After successful save:
    this.originalSettings = JSON.parse(JSON.stringify(this.settings));
    this.hasChanges = false;
  }

  returnToMain() {
    this.return.emit();
  }
}
