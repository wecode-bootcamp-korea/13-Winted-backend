from django.urls import path
from.views       import DuplicationView,SignUpView,SignInView,LikeView

urlpatterns = [
    path('/check',DuplicationView.as_view()),
    path('/sign_up',SignUpView.as_view()),
    path('/sign_in',SignInView.as_view()),
    path('/like'   ,LikeView.as_view()),
]