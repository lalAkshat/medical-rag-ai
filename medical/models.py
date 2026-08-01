from django.db import models
from django.contrib.auth.models import User


class MedicalReport(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    pdf = models.FileField(upload_to="reports/")

    extracted_text = models.TextField(blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    from django.db import models
from django.contrib.auth.models import User


class ChatHistory(models.Model):
    report = models.ForeignKey(
        "MedicalReport",
        on_delete=models.CASCADE
    )

    question = models.TextField()

    answer = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:40]