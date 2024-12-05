"""
URL configuration for essay_evaluator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from evaluator import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from evaluator.views import *



urlpatterns = [
   # A url pattern for the project.
    path('', views.Home.as_view(), name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("evaluate/", views.essay_evaluation_view, name="evaluate"),
    path("evaluate/<str:session_id>/", views.essay_evaluation_view, name="feedback"),
    path("evaluate/status/<str:session_id>/", views.check_feedback_status, name="check_feedback"),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    
]

# Used to serve static files in development mode.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
