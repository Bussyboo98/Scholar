import threading
from .evaluate import evaluate_essay  # Import the essay evaluation function

def evaluate_essay_background(essay_text, callback):
    """
    Run essay evaluation in a background thread and execute the callback with results.
    """
    def task():
        feedback = evaluate_essay(essay_text)
        callback(feedback)

    thread = threading.Thread(target=task)
    thread.start()
