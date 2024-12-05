from django.contrib import admin
from .models import *

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("evaluator", "evaluated_at", "score", "feedback",  "uploaded_at")
    search_fields = ("evaluator__username", "essay_text", "feedback")
    list_filter = ("evaluated_at",)
