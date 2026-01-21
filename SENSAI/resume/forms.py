# resume/forms.py
from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ["user", "created_at"]

class ResumeInputForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    skills = forms.CharField(widget=forms.Textarea)
    experience = forms.CharField(widget=forms.Textarea)

