import { Injectable, PLATFORM_ID, Inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly API_URL = 'http://localhost:8000/users';
  private isLoggedInSubject = new BehaviorSubject<boolean>(false);
  isLoggedIn$ = this.isLoggedInSubject.asObservable();

  constructor(
    @Inject(PLATFORM_ID) private platformId: Object,
    private http: HttpClient
  ) {
    this.checkAuthStatus();
  }

  private checkAuthStatus() {
    if (isPlatformBrowser(this.platformId)) {
      this.isLoggedInSubject.next(!!this.getUserData());
    }
  }

  login(email: string, password: string) {
    return this.http.post(`${this.API_URL}/login`, { email, password });
  }

  register(userData: any) {
    return this.http.post(`${this.API_URL}/register`, userData);
  }

  storeUserData(userId: string) {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem('userData', JSON.stringify({ user_id: userId }));
      this.isLoggedInSubject.next(true);
    }
  }

  getUserData() {
    if (isPlatformBrowser(this.platformId)) {
      const data = localStorage.getItem('userData');
      return data ? JSON.parse(data) : null;
    }
    return null;
  }

  getUserInformation(): Observable<any> {
    if (isPlatformBrowser(this.platformId)) {
      const userData = localStorage.getItem('userData');
      if (!userData) {
        return of(null); // Return observable of null if no data
      }
      
      try {
        const parsedData = JSON.parse(userData);
        return this.http.get(`${this.API_URL}/${parsedData.user_id}`).pipe(
          catchError(error => {
            console.error('API Error:', error);
            return of(null); // Fallback if API fails
          })
        );
      } catch (e) {
        console.error('Parsing error:', e);
        return of(null);
      }
    }
    return of(null); // Server-side fallback
  }

  logout() {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('userData');
      this.isLoggedInSubject.next(false);
    }
  }
}