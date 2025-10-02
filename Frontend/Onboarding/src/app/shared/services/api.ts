import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment.development';

@Injectable({
  providedIn: 'root',
})
export class Api<T, U = T> {
  private apiUrl: string = environment.apiUrl;

  constructor(private http: HttpClient) {}

  get<TOverride = T>(endpoint: string): Observable<TOverride> {
    return this.http.get<TOverride>(`${this.apiUrl}/${endpoint}`, {
      withCredentials: true,
    });
  }

  post<TOverride = T>(
    endpoint: string,
    body: U | null = null
  ): Observable<TOverride> {
    return this.http.post<TOverride>(`${this.apiUrl}/${endpoint}`, body, {
      withCredentials: true,
    });
  }

  put(endpoint: string, body: U): Observable<T> {
    return this.http.put<T>(`${this.apiUrl}/${endpoint}`, body);
  }

  delete<TOverride = T>(endpoint: string): Observable<TOverride> {
    return this.http.delete<TOverride>(`${this.apiUrl}/${endpoint}`, {
      withCredentials: true,
    });
  }
}
