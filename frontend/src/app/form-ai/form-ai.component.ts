import { Component, OnInit } from '@angular/core';
import { AiService } from '../services/ai.service';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap, tap } from 'rxjs/operators';

@Component({
  selector: 'app-form-ai',
  templateUrl: './form-ai.component.html',
  styleUrls: ['./form-ai.component.css']
})
export class FormAiComponent implements OnInit {

  formData: any = {
    name: '',
    email: '',
    age: ''
  };

  aiResponse: any = {
    errors: {},
    suggestions: {},
    autoFill: {}
  };

  loading = false;

  private inputSubject = new Subject<any>();

  constructor(private aiService: AiService) {}

  ngOnInit(): void {

    this.inputSubject.pipe(
      debounceTime(500), // wait for user to stop typing
      distinctUntilChanged((prev, curr) => JSON.stringify(prev) === JSON.stringify(curr)),
      
      tap(() => this.loading = true),

      // 🔥 SWITCHMAP (IMPORTANT)
      switchMap(data => this.aiService.getFormSuggestions(data))
      
    ).subscribe(res => {
      this.aiResponse = res;

      // 🔥 AUTO-FILL
      Object.keys(res.autoFill || {}).forEach(key => {
        if (!this.formData[key]) {
          this.formData[key] = res.autoFill[key];
        }
      });

      this.loading = false;
    });
  }

  onInputChange() {
    this.inputSubject.next({ ...this.formData }); // send copy
  }
  downloadPDF() {
  const finalData = {
    role: this.aiResponse.autoFill?.role || this.formData.role,
    skills: this.aiResponse.autoFill?.skills || this.formData.skills,
    experience: this.aiResponse.autoFill?.experience || this.formData.experience,
    summary: this.aiResponse.autoFill?.summary || this.formData.summary
  };

  this.aiService.downloadResume(finalData).subscribe((blob: Blob) => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'resume.pdf';
    a.click();
  });
}
}