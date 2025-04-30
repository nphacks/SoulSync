import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VoiceJournalComponent } from './voice-journal.component';

describe('VoiceJournalComponent', () => {
  let component: VoiceJournalComponent;
  let fixture: ComponentFixture<VoiceJournalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [VoiceJournalComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(VoiceJournalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
