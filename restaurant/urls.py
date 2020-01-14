from django.urls import path
from .views       import TopTopic, RestaurantView

urlpatterns = [
    path('/topic/<int:topic_id>', TopTopic.as_view()),
    path('/<int:topic_id>', RestaurantView.as_view())
]