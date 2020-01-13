from django.urls import path
from .views      import SignUpView, NicknameCheckView, SignInView, SocialKakaoView

urlpatterns = [
    path('', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/nickname', NicknameCheckView.as_view()),
    path('/kakao', SocialKakaoView.as_view())
]
