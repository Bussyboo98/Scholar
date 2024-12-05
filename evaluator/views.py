from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import TemplateView
from .models import *
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from .forms import EssayUploadForm
from .evaluate import evaluate_essay
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from .utils import evaluate_essay_background
from .models import Evaluation


class Home(FormView):
    template_name = 'index.html'
    form_class = RegisterForm

    def form_valid(self, form):
        # Save the user
        form.save()

        messages.success(self.request, "Registration successful! You can now log in.")
        return redirect("login")  

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:

            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid Username and Password')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')


results = {}

def essay_evaluation_view(request, session_id=None):
    """
    Handles all aspects of essay evaluation: submission, processing, and feedback display.
    """
    if request.method == "POST":
        form = EssayUploadForm(request.POST, request.FILES)
        if form.is_valid():
            essay_text = form.cleaned_data.get("essay_text")
            essay_file = form.cleaned_data.get("essay_file")

            # Handle file upload if provided
            if essay_file:
                essay_text = essay_file.read().decode("utf-8")

            # Generate a unique session ID
            session_id = str(uuid.uuid4())
            results[session_id] = None  

            def callback(feedback):
                results[session_id] = feedback  
                
                predicted_score = feedback.get("predicted_score")
                detailed_feedback = feedback.get("feedback")
                final_score = feedback.get("final_score")

                # Save the evaluation in the database
                Evaluation.objects.create(
                    evaluator=request.user,
                    essay_text=essay_text,
                    essay_file=essay_file if essay_file else None,
                    score=final_score,
                    feedback=detailed_feedback,
                )
                if essay_file:
                    evaluation.essay_file.save(essay_file.name, essay_file)
                    
                Evaluation.save()

            evaluate_essay_background(essay_text, callback)
            return render(request, "processing.html", {"session_id": session_id})
    elif session_id:
       
        feedback = results.get(session_id)
        if feedback:
            return render(request, "feedback.html", {"feedback": feedback})
        else:
            return render(request, "processing.html", {"session_id": session_id})
    
    form = EssayUploadForm()
    return render(request, "evaluate.html", {"form": form})

def check_feedback_status(request, session_id):
    """
    API endpoint to check the evaluation status for a session.
    """
    feedback = results.get(session_id)
    if feedback:
        return JsonResponse({"status": "complete", "feedback": feedback})
    return JsonResponse({"status": "processing"})