import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  selectedTab = 0;
  loginForm: FormGroup;
  signupForm: FormGroup;
  isLoading = false;

  constructor(
    private fb: FormBuilder,
    private snackBar: MatSnackBar,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });

    this.signupForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      isTherapist: [false]
    });
  }

  onLogin() {
    if (this.loginForm.invalid) return;
    this.isLoading = true;

    const { email, password } = this.loginForm.value;
    this.authService.login(email, password).subscribe({
      next: (response: any) => {
        if (response.success) {
          this.authService.storeUserData(response.user_id);
          this.router.navigate(['/']);
        }
      },
      error: (error) => this.handleError(error, 'Login'),
      complete: () => this.isLoading = false
    });
  }

  onSignup() {
    if (this.signupForm.invalid) return;
    this.isLoading = true;

    const userData = this.buildSignupPayload();
    console.log(userData)
    this.authService.register(userData).subscribe({
      next: (response: any) => {
        if (response.success) {
          this.authService.storeUserData(response.user_id);
          this.snackBar.open('Registration successful!', 'Close', { duration: 3000 });
          this.selectedTab = 0;
        }
      },
      error: (error) => this.handleError(error, 'Registration'),
      complete: () => this.isLoading = false
    });
  }

  private buildSignupPayload() {
    const { name, email, password, isTherapist } = this.signupForm.value;
    return {
      name,
      email,
      password,
      user_type: isTherapist ? 'therapist' : 'patient',
      settings: {
        therapist: { name: '', email: '' },
        sentimentShare: false,
        emotionShare: false,
        topicShare: false,
        summaryShare: false,
        extremeEmotions: false
      }
    };
  }

  private handleError(error: any, action: string) {
    const message = error.error?.message || 'Unknown error occurred';
    this.snackBar.open(`${action} failed: ${message}`, 'Close', { duration: 3000 });
    this.isLoading = false;
  }
}
