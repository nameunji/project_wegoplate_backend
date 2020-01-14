import json

from .models          import *
from user.models      import Review, Review_Star

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg

class TopTopic(View):
    def get(self, request, topic_id):

        try:
            topic_top_list = Topic_Top_list.objects.select_related('topic', 'top_list').filter(topic__id = topic_id)
            topic_title = topic_top_list[0].topic.title

            toplists = [{
                'id' : toplist.top_list.id,
                'title' : toplist.top_list.title,
                'description' : toplist.top_list.description,
                'image' : toplist.top_list.image
            } for toplist in topic_top_list ]

            return JsonResponse({'title' : topic_title, 'top_list' : toplists}, status=200)
        except Topic.DoesNotExist:
            return JsonResponse({'result' : 'DOES_NOT_EXIST_TOPIC'}, status = 400)


class RestaurantView(View):
    def get(self, request, topic_id):
        restaurants = Topic_Restaurant.objects.select_related('topic','restaurant').filter(topic_id = topic_id)

        if restaurants.exists():  
            topic_title = restaurants[0].topic.title
            restaurant_list= [{
                'id'    : el.restaurant.id,
                'name'  : el.restaurant.name,
                'state' : el.restaurant.location_state.state,
                'food'  : el.restaurant.food.category,
                'image' : el.restaurant.restaurant_image_set.get(restaurant_id = el.restaurant.id).images,
                'grade' : el.restaurant.review_set.filter(restaurant_id = el.restaurant.id).values('review_star__star').aggregate(avg=Avg('review_star__star'))['avg']
            } for el in restaurants]
            return JsonResponse({"title" : topic_title, "restaurant_list" : restaurant_list}, status=200)
        else:
            return JsonResponse({"message":"DOES_NOT_EXIST_TOPIC"}, status = 400)