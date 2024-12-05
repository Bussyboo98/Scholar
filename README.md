Scholar 📝

Scholar is a Python and Django-based web application that evaluates and scores essays using machine learning. It provides users with detailed feedback on essay content, grammar, and structure, helping students improve their writing skills.

Features
Upload essays as text or files.
Automatic scoring of essays based on content, grammar, and structure.
Detailed feedback to help improve writing.
User-friendly interface for seamless interaction.
Technologies Used
Backend: Python, Django
Frontend: Django templates (HTML/CSS/JavaScript)
Machine Learning: Transformer-based model (DeBERTa) for essay evaluation
Database: MySQL
Others: Swagger for API documentation, TinyMCE for text editing

Installation
Prerequisites
Python 3.9+
MySQL
Pipenv or pip for dependency management
Setup Instructions
Clone the Repository


git clone https://github.com/your-username/scholar.git  
cd essay_evaluator
Set up a Virtual Environment

python -m venv venv  
source venv/bin/activate    # On Windows: venv\Scripts\activate  


Install Dependencies
pip install -r requirements.txt  
Set up the Database

Configure your database settings in settings.py:

DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'scholar_db',  
        'USER': 'your_db_user',  
        'PASSWORD': 'your_db_password',  
        'HOST': 'localhost',  
        'PORT': '3306',  
    }  
}  
Run migrations:

python manage.py makemigrations  
python manage.py migrate  
Train the Machine Learning Model (Optional)


python manage.py runserver  
Open your browser and navigate to http://127.0.0.1:8000/.
