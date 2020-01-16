from django.urls  import path
from .views       import (
    TopTopic,
    RestaurantView,
    DetailTopImage,
    RestaurantDetailInfoView,
    RestaurantDetailToplistView,
    DetailReview,
    RestaurantNearView,
    RestaurantDetailToplistRelatedView,
    RestaurantTagview,
    RestaurantEatDealView,
    RestaurantEatDealSearchView,
    SearchView,
    SearchFinalView
)
urlpatterns = [
    path('/topic/<int:topic_id>', TopTopic.as_view()),
    path('/<int:topic_id>', RestaurantView.as_view()),
    path('/<int:restaurant_id>/topimage', DetailTopImage.as_view()),
    path('/<int:restaurant_id>/info', RestaurantDetailInfoView.as_view()),
    path('/<int:restaurant_id>/toplist', RestaurantDetailToplistView.as_view()),
    path('/<int:restaurant_id>/review', DetailReview.as_view()),
    path('/<int:restaurant_id>/near', RestaurantNearView.as_view()),
    path('/<int:restaurant_id>/related', RestaurantDetailToplistRelatedView.as_view()),
    path('/<int:restaurant_id>/tag', RestaurantTagview.as_view()),
    path('/eat_deal', RestaurantEatDealView.as_view()),
    path('/eat_deal_search', RestaurantEatDealSearchView.as_view()),
    path('/keyword', SearchView.as_view()),
    path('/search/<str:text>', SearchFinalView.as_view()),
]
