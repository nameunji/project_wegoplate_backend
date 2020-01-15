from django.urls import path
from .views       import TopTopic, RestaurantView, DetailTopImage

urlpatterns = [
    path('/topic/<int:topic_id>', TopTopic.as_view()),
    path('/<int:topic_id>', RestaurantView.as_view()),
    path('/<int:restaurant_id>/topimage', DetailTopImage.as_view()),
]


