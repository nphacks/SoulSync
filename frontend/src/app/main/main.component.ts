import { Component, HostListener, Inject } from '@angular/core';
import { VoiceJournalComponent } from './voice-journal/voice-journal.component';
import { TextJournalComponent } from './text-journal/text-journal.component';
import { HandwrittenJournalComponent } from './handwritten-journal/handwritten-journal.component';
import { BotJournalComponent } from './bot-journal/bot-journal.component';
import { isPlatformBrowser } from '@angular/common';
import { PLATFORM_ID } from '@angular/core';

// In your component class:



@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrl: './main.component.scss'
})
export class MainComponent {
  cards = [
    { component: TextJournalComponent },
    { component: HandwrittenJournalComponent },
    { component: VoiceJournalComponent },
    { component: BotJournalComponent }
  ];

  // currentPosition = 0;
  isDragging = false;
  startX = 0;
  currentTranslate = 0;
  activeIndex = 2; // This will make VoiceJournalComponent appear first
  currentPosition = -2 * this.cardWidth

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}


  get cardWidth() {
    return isPlatformBrowser(this.platformId) ? window.innerWidth * 0.8 : 0;
  }

  prevSlide() {
    if (this.activeIndex > 0) {
      this.activeIndex--;
      this.currentPosition += this.cardWidth;;
      this.currentTranslate = this.currentPosition;
    }
  }

  nextSlide() {
    if (this.activeIndex < this.cards.length - 1) {
      this.activeIndex++;
      this.currentPosition -= this.cardWidth;;
      this.currentTranslate = this.currentPosition;
    }
  }

  startDrag(event: MouseEvent) {
    this.isDragging = true;
    this.startX = event.clientX;
  }

  onDrag(event: MouseEvent) {
    if (!this.isDragging) return;
    const movedBy = event.clientX - this.startX;
    this.currentPosition = this.currentTranslate + movedBy;
  }

  endDrag() {
    this.isDragging = false;
    
    // Determine slide change based on drag distance
    const movedBy = this.currentPosition - this.currentTranslate;
    if (movedBy < -100 && this.activeIndex < this.cards.length - 1) {
      this.nextSlide();
    } else if (movedBy > 100 && this.activeIndex > 0) {
      this.prevSlide();
    } else {
      // Return to original position if not moved enough
      this.currentPosition = this.currentTranslate;
    }
  }
}
