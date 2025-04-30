import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HandwrittenJournalComponent } from './handwritten-journal.component';

describe('HandwrittenJournalComponent', () => {
  let component: HandwrittenJournalComponent;
  let fixture: ComponentFixture<HandwrittenJournalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HandwrittenJournalComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HandwrittenJournalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
