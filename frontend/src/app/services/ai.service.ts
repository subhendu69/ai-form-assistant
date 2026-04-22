import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AiService {

  private API_URL = 'http://127.0.0.1:8000/form-ai';

  constructor(private http: HttpClient) {}

  getFormSuggestions(data: any): Observable<any> {
    return this.http.post(this.API_URL, data);
  }
}