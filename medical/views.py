from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import MedicalReport, ChatHistory
from .utils import extract_text_from_pdf
from .ai import ask_ai


# ================= HOME =================

@login_required(login_url="login")
def home(request):
    return render(request, "medical/home.html")


# ================= LOGIN =================

def login_page(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Invalid Email or Password")

    return render(request, "medical/login.html")


# ================= REGISTER =================

def register_page(request):

    if request.method == "POST":

        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=fullname
        )

        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "medical/register.html")


# ================= LOGOUT =================

def logout_page(request):

    logout(request)

    return redirect("login")


# ================= UPLOAD PDF =================

@login_required(login_url="login")
def upload_page(request):

    extracted_text = ""

    if request.method == "POST":

        title = request.POST.get("title")
        pdf = request.FILES.get("pdf")

        report = MedicalReport.objects.create(
            user=request.user,
            title=title,
            pdf=pdf
        )

        extracted_text = extract_text_from_pdf(report.pdf.path)

        report.extracted_text = extracted_text
        report.save()

        messages.success(request, "PDF Uploaded Successfully!")

    return render(
        request,
        "medical/upload.html",
        {
            "text": extracted_text
        }
    )


# ================= REPORTS =================

@login_required(login_url="login")
def reports_page(request):

    reports = MedicalReport.objects.filter(
        user=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "medical/reports.html",
        {
            "reports": reports
        }
    )


# ================= DELETE REPORT =================

@login_required(login_url="login")
def delete_report(request, report_id):

    report = MedicalReport.objects.get(
        id=report_id,
        user=request.user
    )

    report.delete()

    messages.success(request, "Report Deleted Successfully!")

    return redirect("reports")


# ================= AI CHAT =================

@login_required(login_url="login")
def chat_page(request, report_id):

    report = MedicalReport.objects.get(
        id=report_id,
        user=request.user
    )

    answer = ""
    question = ""

    # Load previous chat history
    history = ChatHistory.objects.filter(
        report=report
    ).order_by("-created_at")

    if request.method == "POST":

        question = request.POST.get("question")

        answer = ask_ai(
            question,
            report.extracted_text
        )

        # Save Question & Answer
        ChatHistory.objects.create(
            report=report,
            question=question,
            answer=answer
        )

        # Reload history
        history = ChatHistory.objects.filter(
            report=report
        ).order_by("-created_at")

    return render(
        request,
        "medical/chat.html",
        {
            "report": report,
            "question": question,
            "answer": answer,
            "history": history
        }
    )