import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BotJournalComponent } from './bot-journal.component';

describe('BotJournalComponent', () => {
  let component: BotJournalComponent;
  let fixture: ComponentFixture<BotJournalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [BotJournalComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(BotJournalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
