import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {
  private apiUrl = 'http://localhost:8000/chatbot/chat/';

  constructor(private http: HttpClient) { }

  postMessage(data: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, data);
  }
}

// I am learning how to enrich the beauty of nature. The nature has been so beautiful and honest but we hardly look at it. I am thinking of picking up a new hobby that makes it worthwhile.

// I am not too good at painting, but photography sounds good. I like knowing about camera, that would not only keep me closer to flora but also fauna.
