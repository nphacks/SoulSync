import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TextJournalComponent } from './text-journal.component';

describe('TextJournalComponent', () => {
  let component: TextJournalComponent;
  let fixture: ComponentFixture<TextJournalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TextJournalComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TextJournalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
