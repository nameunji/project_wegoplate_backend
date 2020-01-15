import json

from .models          import *
from user.models      import Review, Review_image, Review_Star

from django.views     import View
from django.db.models import Avg
from django.http      import JsonResponse, HttpResponse

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


class DetailTopImage(View):
    def get(self, request, restaurant_id):
        image = Restaurant_image.objects.filter(restaurant_id = restaurant_id).values_list('images', flat=True)

        return JsonResponse({'image' : list(image)})

class RestaurantDetailInfoView(View):
    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.select_related('price_range', 'food', 'location_city', 'location_state', 'location_road', 'holiday').prefetch_related('menu_set','restaurant_info_set').get(id=restaurant_id)

            title_dict = { "parking":"주차", "number":"전화번호", "last_order":"마지막주문", "site":"웹 사이트", "breaktime":"쉬는시간", "opening_hours":"영업시간"}

            result = []
            # address
            result.append({
                "title"   : "주소",
                "content" : ['{} {} {} {}'.format(restaurant.location_city.city, restaurant.location_state.state, restaurant.location_road.road, restaurant.location_detail)] 
            })
            # food
            result.append({
                "title"   : "음식 종류",
                "content" : [restaurant.food.category]
            })
            # price
            result.append({
                "title"   : "가격대",
                "content" : [restaurant.price_range.price_range]
            })
            # holiday
            result.append({
                "title"   : "휴일",
                "content" : [restaurant.holiday.holiday] 
            })
            
            info = restaurant.restaurant_info_set.values().get(restaurant_id = restaurant_id)
            for el in info :
                if el in title_dict and info[el] != None :
                    result.append({"title" : title_dict[el], "content" : [info[el]]})

            # menu
            result.append({
                "title"   : "메뉴",
                "content" : [
                    {
                        "menu"  : el.menu,
                        "price" : el.price 
                    }
                    for el in restaurant.menu_set.filter(restaurant_id=restaurant_id) ]
            })

            return JsonResponse({"result":result}, status = 200)
        except Restaurant.DoesNotExist:
            return HttpResponse(status = 404)

class RestaurantDetailToplistView(View):
    def get(self, request, restaurant_id):
        toplists = Top_lists_Restaurant.objects.select_related('top_list', 'restaurant').filter(restaurant_id=restaurant_id)

        if toplists.exists():
            toplist = [
                {
                    "id"          : el.top_list.id,
                    "title"       : el.top_list.title,
                    "description" : el.top_list.description,
                    "image"       : el.top_list.image
                } for el in toplists]
            return JsonResponse({"result" : toplist}, status = 200)
        else:
            return HttpResponse(status = 404)


