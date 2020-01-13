from django.urls import path
from .views import TopTopic

urlpatterns = [
    path('/topic/<int:topic_id>', TopTopic.as_view())
]
