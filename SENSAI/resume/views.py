from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ResumeForm
from .models import Resume


@login_required
def create_resume(request):
    if request.method == "POST":
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect("resume_preview", resume_id=resume.id)
    else:
        form = ResumeForm()

    return render(request, "resume/create_resume.html", {"form": form})


@login_required
def resume_preview(request, resume_id):
    resume = Resume.objects.get(id=resume_id, user=request.user)
    return render(request, "resume/resume_preview.html", {"resume": resume})

# @login_required
# def create_resume(request):
#     if request.method == "POST":
#         form = ResumeInputForm(request.POST)
#         if form.is_valid():
#             resume_text = generate_ats_resume(form.cleaned_data)

#             resume = Resume.objects.create(
#                 user=request.user,
#                 content=resume_text
#             )

#             return redirect("resume_preview", id=resume.id)
#     else:
#         form = ResumeInputForm()

#     return render(request, "resume/create_resume.html", {"form": form})