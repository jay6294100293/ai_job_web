from django.urls import path
from . import views
from .views.extraa_keyword_view import extract_keywords_view
from .views.job_input_view import job_input

urlpatterns = [
    path('job-input/', job_input, name='job_input'),
    path('extract-keywords/<int:job_input_id>/', extract_keywords_view, name='extract_keywords'),
]
