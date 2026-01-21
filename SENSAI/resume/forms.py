from django import forms

class ResumeForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    linkedin = forms.URLField(required=False)

    target_role = forms.CharField(max_length=100)
    industry = forms.CharField(max_length=100)

    skills = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Comma separated skills"
    )

    experience = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6}),
        help_text="Describe your experience briefly"
    )

    education = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3})
    )