from django.urls import path, include

urlpatterns = [
    path('company', include('company.urls')),
    path('resume', include('resume.urls')),
    path('recommend', include('recommend.urls')),
]
