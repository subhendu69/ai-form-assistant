import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormAiComponent } from './form-ai.component';

describe('FormAiComponent', () => {
  let component: FormAiComponent;
  let fixture: ComponentFixture<FormAiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormAiComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FormAiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
