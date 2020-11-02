from django.urls import path

from recommend.views import KakaoMessageView, RecommenderView
urlpatterns = [
    path('', RecommenderView.as_view()),
    path('/send-kakaotalk', KakaoMessageView.as_view())
]