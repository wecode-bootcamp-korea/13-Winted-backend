from django.urls import path

from resume.views import (
    ResumeListView, 
    ResumeDetailListView,
    UserCareerView,
    EducationView,
    AwardView,
    ForeignLanguageView
)

urlpatterns = [
    path('', ResumeListView.as_view()),
    path('/<int:resume_id>', ResumeDetailListView.as_view()),
    path('/<int:resume_id>/career', UserCareerView.as_view()),
    path('/<int:resume_id>/education', EducationView.as_view()),
    path('/<int:resume_id>/award', AwardView.as_view()),
    path('/<int:resume_id>/language', ForeignLanguageView.as_view()),
]