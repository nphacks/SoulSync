import { Component, ElementRef, ViewChild, OnDestroy, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { MatSnackBar } from '@angular/material/snack-bar';
import { JournalEntryService } from '../../services/journal-entry.service';

@Component({
  selector: 'app-voice-journal',
  templateUrl: './voice-journal.component.html',
  styleUrl: './voice-journal.component.scss'
})
export class VoiceJournalComponent {
  private recorder: any;
  private stream: MediaStream | null = null;
  private timer: any;
  private startTime: number | null = null;

  private readonly recordingDuration = 60; // 60 seconds = 1 minute
  readonly circleCircumference = 2 * Math.PI * 180; // 2πr
  
  isRecording = false;
  remainingTime = this.recordingDuration;
  audioUrl: string | null = null;
  circleDashOffset = this.circleCircumference;
  hasRecorded = false;

  audioBlob: Blob | null = null;
  isSaving = false;

  constructor(
    @Inject(PLATFORM_ID) private platformId: Object,
    private journalEntryService: JournalEntryService,
    private snackBar: MatSnackBar
  ) {}

  async toggleRecording() {
    if (!isPlatformBrowser(this.platformId) || this.isRecording) return;

    this.isRecording = true;
    
    this.remainingTime = this.recordingDuration;
    this.circleDashOffset = this.circleCircumference;
    
    try {
      const RecordRTC = (await import('recordrtc')).default;
      this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.recorder = new RecordRTC.StereoAudioRecorder(this.stream, {
        type: 'audio',
        mimeType: 'audio/wav'
      });
      
      this.recorder.record();
      
      this.timer = setInterval(() => {
        const now = Date.now();
        if (!this.startTime) {
          this.startTime = now;
        }
        
        const elapsedSeconds = (now - this.startTime) / 1000;
        this.remainingTime = Math.max(0, this.recordingDuration - elapsedSeconds);
        const progress = elapsedSeconds / this.recordingDuration;
        this.circleDashOffset = this.circleCircumference * (1 - progress);
        
        if (this.remainingTime <= 0) {
          this.stopRecording();
        }
      }, 50);
      
    } catch (error) {
      console.error('Error:', error);
      this.isRecording = false;
    }
  }

  stopRecording() {
    this.startTime = null;
    clearInterval(this.timer);
    
    if (this.recorder) {
      this.recorder.stop((blob: Blob) => {
        this.audioBlob = blob;
        this.audioUrl = URL.createObjectURL(blob);
        this.isRecording = false;
        
        if (this.stream) {
          this.stream.getTracks().forEach(track => track.stop());
          this.stream = null;
        }
        this.hasRecorded = true
      });
    }
  }

  async saveTheJournalEntry() {
    if (!this.hasRecorded || !this.audioBlob) {
      this.snackBar.open('Please record an entry first', 'Close', { duration: 3000 });
      return;
    }

    this.isSaving = true;

    try {
      await this.journalEntryService.uploadAudioEntry(this.audioBlob);
      this.snackBar.open('Journal entry saved successfully!', 'Close', { duration: 3000 });
      this.resetRecording();
    } catch (error) {
      console.error('Error saving entry:', error);
      this.snackBar.open('Failed to save entry: ' + error, 'Close', { duration: 3000 });
    } finally {
      this.isSaving = false;
    }
  }

  private resetRecording() {
    this.hasRecorded = false;
    this.audioBlob = null;
    if (this.audioUrl) {
      URL.revokeObjectURL(this.audioUrl);
      this.audioUrl = null;
    }
  }

  formatTime(seconds: number): string {
    const wholeSeconds = Math.floor(seconds);  // Add this line
    const mins = Math.floor(wholeSeconds / 60);  // Use wholeSeconds
    const secs = wholeSeconds % 60;  // Use wholeSeconds
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  }

  ngOnDestroy() {
    if (this.isRecording) this.stopRecording();
    if (this.audioUrl) URL.revokeObjectURL(this.audioUrl);
  }
}
