import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({ providedIn: 'root' })
export class JournalEntryService {
  private readonly API_URL = 'http://localhost:8000/journal_entry';

  constructor(private http: HttpClient) {}

  async uploadAudioEntry(audioBlob: Blob): Promise<any> {
    // Get user_id directly from localStorage
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    const userId = userData.user_id;

    if (!userId) {
      return Promise.reject('User not authenticated');
    }

    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.wav');
    formData.append('user_id', userId);
    const response = await this.http.post(`${this.API_URL}/audio/`, formData)
    return response 
  }

  addTextEntry(text: string): Promise<any> {
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    const userId = userData.user_id;
  
    if (!userId) {
      return Promise.reject('User not authenticated');
    }
  
    const formData = new FormData();
    formData.append('user_id', userId);
    formData.append('text', text);
  
    return this.http.post(`${this.API_URL}/text/`, formData).toPromise();
  }

  uploadDocumentEntry(file: File): Promise<any> {
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    const userId = userData.user_id;
  
    if (!userId) {
      return Promise.reject('User not authenticated');
    }
  
    const formData = new FormData();
    formData.append('document', file, file.name);
    formData.append('user_id', userId);
  
    return this.http.post(`${this.API_URL}/image/`, formData).toPromise();
  }

  addChatbotEntry(data: any): Promise<any> {
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    const userId = userData.user_id;
  
    if (!userId) {
      return Promise.reject('User not authenticated');
    }
  
    const formData = new FormData();
    formData.append('user_id', userId);
    formData.append('conversation', JSON.stringify(data));
  
    return this.http.post(`${this.API_URL}/chatbot/`, formData).toPromise();
  }
}