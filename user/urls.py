from django.urls import path
from .views      import SignUpView, NicknameCheckView

urlpatterns = [
    path('', SignUpView.as_view()),
    path('/nickname', NicknameCheckView.as_view())
]
