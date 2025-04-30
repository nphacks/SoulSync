import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatList } from '@angular/material/list';
import { ChatbotService } from '../../services/chatbot.service';
import { JournalEntryService } from '../../services/journal-entry.service';

interface Message {
  role: 'system' | 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

@Component({
  selector: 'app-bot-journal',
  templateUrl: './bot-journal.component.html',
  styleUrls: ['./bot-journal.component.scss']
})
export class BotJournalComponent implements OnInit {
  @ViewChild(MatList) messageList!: MatList;

  messages: Message[] = [];

  messageControl = new FormControl('', [Validators.required]);
  isSending = false;
  userId: string = '';
  isSaving = false

  constructor(
    private snackBar: MatSnackBar,
    private chatbotService: ChatbotService,
    private journalEntryService: JournalEntryService
  ) {}

  ngOnInit(): void {
    this.getUserId();
  }

  getUserId(): void {
    const userData = localStorage.getItem('userData');
    if (userData) {
      try {
        const parsedData = JSON.parse(userData);
        this.userId = parsedData.user_id;
      } catch (e) {
        console.error('Error parsing user data', e);
      }
    }
  }

  sendMessage(): void {
    if (this.messageControl.invalid || !this.userId) return;

    const userMessage = this.messageControl.value!;
    this.addMessage('user', userMessage);
    this.messageControl.reset();
    this.isSending = true;

    const request = {
      user_id: this.userId,
      user_message: userMessage,
      conversation: this.getConversationHistory()
    };

    this.chatbotService.postMessage(request).subscribe({
      next: (response: any) => {
        this.addMessage('assistant', response.response);
        this.isSending = false;
      },
      error: (error: any) => {
        console.error('Error sending message', error);
        this.snackBar.open('Error sending message', 'Close', { duration: 3000 });
        this.isSending = false;
      }
    });
  }

  async addJournalEntry() {
    this.isSaving = true;
    
    try {
      await this.journalEntryService.addChatbotEntry(this.getConversationHistory());
      this.snackBar.open('Journal entry saved successfully!', 'Close', { duration: 3000 });
      this.resetConversation();
    } catch (error) {
      console.error('Error saving entry:', error);
      this.snackBar.open('Failed to save entry', 'Close', { duration: 3000 });
    } finally {
      this.isSaving = false;
    }
  }

  resetConversation() {
    this.messages = [];
}

  private addMessage(role: 'user' | 'assistant' | 'system', content: string): void {
    const newMessage: Message = {
      role,
      content,
      timestamp: new Date()
    };
    this.messages.push(newMessage);
    this.scrollToBottom();
  }

  private getConversationHistory(): any[] {
    return this.messages
      .filter(msg => msg.role !== 'system')
      .map(msg => ({
        role: msg.role,
        content: msg.content
      }));
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      if (this.messageList) {
        const listElement = (this.messageList as any)._elementRef.nativeElement;
        listElement.scrollTop = listElement.scrollHeight;
      }
    }, 100);
  }
}