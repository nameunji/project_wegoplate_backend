from django.urls import path,include

urlpatterns = [
    path('restaurant', include('restaurant.urls'))
]
