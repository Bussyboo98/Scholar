from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User



class Evaluation(models.Model):
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="evaluations")
    essay_text = HTMLField()
    essay_file = models.FileField(upload_to="evaluations/files/", null=True, blank=True, verbose_name="Uploaded File")
    evaluated_at = models.DateTimeField(auto_now_add=True, verbose_name="Evaluated On")
    score = models.FloatField(null=True, blank=True, verbose_name="Evaluation Score")
    feedback = models.TextField(null=True, blank=True, verbose_name="Feedback")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Evaluation by {self.evaluator.username} on {self.evaluated_at}"