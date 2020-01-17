import json

from .models          import *
from user.models      import Review, Review_image, Review_Star
from user.utils       import login_decorator

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
                'id'    : element.restaurant.id,
                'name'  : element.restaurant.name,
                'state' : element.restaurant.location_state.state,
                'food'  : element.restaurant.food.category,
                'image' : element.restaurant.restaurant_image_set.get(restaurant_id = element.restaurant.id).images,
                'grade' : element.restaurant.review_set.filter(restaurant_id = element.restaurant.id).values('review_star__star').aggregate(avg=Avg('review_star__star'))['avg']
            } for element in restaurants]
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
            for element in info :
                if element in title_dict and info[element] != None :
                    result.append({"title" : title_dict[element], "content" : [info[element]]})

            # menu
            result.append({
                "title"   : "메뉴",
                "content" : [
                    {
                        "menu"  : element.menu,
                        "price" : element.price 
                    }
                    for element in restaurant.menu_set.filter(restaurant_id=restaurant_id) ]
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
                    "id"          : element.top_list.id,
                    "title"       : element.top_list.title,
                    "description" : element.top_list.description,
                    "image"       : element.top_list.image
                } for element in toplists]
            return JsonResponse({"result" : toplist}, status = 200)
        else:
            return HttpResponse(status = 404)

class DetailReview(View):
    def get(self,request, restaurant_id):

        offset = request.GET.get('offset',0)
        limit = request.GET.get('limit', 5)
        review_star = request.GET.get('taste', 4)

        restaurant_review = Review.objects.select_related('user','review_star').prefetch_related('review_image_set').filter(restaurant_id = restaurant_id)
    
        if review_star == 4:
            restaurant_rate = restaurant_review.order_by('-create_at')
        else:
            restaurant_rate = restaurant_review.filter(review_star_id = review_star).order_by('-create_at')

        reviews = [
            {
                'name' : review.user.nick_name,
                'rating' : review.review_star.content,
                'text' : review.content,
                'imglist' : list(review.review_image_set.values_list('image', flat=True)),
                'time' : str(review.create_at.year) + '-' + 
                           str(review.create_at.month) + '-' + 
                           str(review.create_at.day)
            }
        for review in list(restaurant_rate[int(offset):int(limit)])]

        return JsonResponse(
            {
                'total_count' : restaurant_rate.count(),
                'good_count' : restaurant_rate.filter(review_star_id = 1).count(),
                'soso_count' : restaurant_rate.filter(review_star_id = 2).count(),
                'bad_count' :restaurant_rate.filter(review_star_id = 3).count(),
                'result' : reviews
            }
        )
        
    @login_decorator
    def post(self, request, restaurant_id):
        data = json.loads(request.body)
        user = request.user
        
        Review(
            user           = user,
            restaurant_id  = data["restaurant_id"],
            content        = data["content"],
            review_star    = Review_Star.objects.get(content = data["star"])
        ).save()
        return HttpResponse(status = 200)

class RestaurantNearView(View):
    def get(self, request, restaurant_id):
        try:
            location_state = Restaurant.objects.get(id = restaurant_id).location_state
            around_restaurant = Restaurant.objects.select_related('food','location_state','price_range').prefetch_related('restaurant_image_set','review_set').filter(location_state_id = location_state.id)

            restaurants = [
                {
                    'id' : restaurant.id,
                    'title' : restaurant.name,
                    'food' :restaurant.food.category,
                    'price' : restaurant.price_range.price_range,
                    'location' : restaurant.location_state.state,
                    'img' : restaurant.restaurant_image_set.values('images')[0],
                    'avg' : restaurant.review_set.filter(restaurant_id = restaurant.id).values('review_star__star').aggregate(avg=Avg('review_star__star'))['avg']
                }
            for restaurant in list(around_restaurant)[:4]]

            return JsonResponse({'result' : restaurants}, status = 200)
        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"DOES_NOT_EXIST_RESTAURANT"}, status = 400)

class RestaurantDetailToplistRelatedView(View):
    def get(self, request, restaurant_id):
        try:
            toplist_id    = Top_lists_Restaurant.objects.filter(restaurant_id=restaurant_id).select_related('top_list').order_by('top_list__create_at')[0].top_list_id
            restaurants   = Top_lists_Restaurant.objects.select_related('top_list','restaurant').filter(top_list_id = toplist_id)[:4]
            toplist_title = restaurants[0].top_list.title

            restaurant_list = [{
                'id'    : element.restaurant.id,
                'name'  : element.restaurant.name,
                'state' : element.restaurant.location_state.state,
                'food'  : element.restaurant.food.category,
                'image' : element.restaurant.restaurant_image_set.get(restaurant_id = element.restaurant.id).images,
                'grade' : element.restaurant.review_set.filter(restaurant_id = element.restaurant.id).values('review_star__star').aggregate(avg=Avg('review_star__star'))['avg']
            } for element in restaurants]

            return JsonResponse({"title" : toplist_title, "restaurant_list" : restaurant_list}, status=200)

        except IndexError:
            return HttpResponse(status = 400)

class RestaurantTagview(View):
    def get(self, request, restaurant_id):

        restaurant_tags = Restaurant_Tag.objects.select_related('restaurant','tag').filter(restaurant_id = restaurant_id)
        tags = [
            {   
                'id' : tag.tag.id,
                'tag' : tag.tag.tag
            }
        for tag in restaurant_tags]

        return JsonResponse({'result' : tags}, status = 200)

class RestaurantEatDealView(View):
    def get(self,request):
        
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 20))

        eat_deal_list = Eat_Deal.objects.select_related('restaurant')[offset * limit:(offset + 1) * limit]
        eat_deals = [
            {
                'offset' : offset,
                'eat_deal_id' :eat_deal.id,
                'title' : eat_deal.restaurant.name,
                'restaurant_id' : eat_deal.restaurant.id,
                'image' : list(eat_deal.restaurant.restaurant_image_set.values('images'))[0],
                'menu' : eat_deal.menu,
                'discount_rate' : eat_deal.discount_rate,
                'price' : int(eat_deal.price),
                'discounted_price' : int(eat_deal.price) - (int(eat_deal.price) * int(eat_deal.discount_rate)/100)
            }
        for eat_deal in list(eat_deal_list)]

        return JsonResponse({'result' : eat_deals}, status=200)

class RestaurantEatDealSearchView(View):
    def get(self, request):

        eat_deal_list = request.GET.getlist('list')

        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 20))

        eat_deal_list = Eat_Deal.objects.select_related('restaurant').filter(restaurant__location_state__in = eat_deal_list)[offset * limit:(offset + 1) * limit]
        eat_deals = [
            {
                'offset' : offset,
                'eat_deal_id' :eat_deal.id,
                'title' : eat_deal.restaurant.name,
                'restaurant_id' : eat_deal.restaurant.id,
                'image' : list(eat_deal.restaurant.restaurant_image_set.values('images'))[0],
                'menu' : eat_deal.menu,
                'discount_rate' : eat_deal.discount_rate,
                'price' : int(eat_deal.price),
                'discounted_price' : int(eat_deal.price) - (int(eat_deal.price) * int(eat_deal.discount_rate)/100)
            }
        for eat_deal in list(eat_deal_list)]

        return JsonResponse({'result' : eat_deals}, status=200)

class SearchView(View):
    def get(self, request):
        data = request.GET.get('text', None)

        restaurants = Restaurant.objects.filter(name__icontains = data)
        result = [restaurant.name for restaurant in restaurants]

        return JsonResponse({"result":result}, status =200)

class SearchFinalView(View):
    def get(self, request, text):
        restaurants = Restaurant.objects.select_related('food', 'location_city', 'location_state', 'location_road').filter(name__icontains = text)

        if restaurants.exists():  
            restaurant_list= [{
                'id'     : element.id,
                'name'   : element.name,
                'state'  : element.location_state.state,
                'address': '{} {} {} {}'.format(element.location_city.city, element.location_state.state, element.location_road.road, element.location_detail),
                'food'   : element.food.category,
                'image'  : element.restaurant_image_set.filter(restaurant_id = element.id)[0].images,
                'grade'  : element.review_set.filter(restaurant_id = element.id).values('review_star__star').aggregate(avg=Avg('review_star__star'))['avg']
            } for element in restaurants]
            return JsonResponse({"restaurant_list" : restaurant_list}, status=200)
        else:
            return JsonResponse({"message":"VALUE_DOES_NOT_EXIST"}, status = 400)

class RestaurantEatDealDetail(View):
    def get(self, request, eat_deal_id):
        try:
            eat_deal_detail = Eat_Deal.objects.select_related('restaurant').get(id = eat_deal_id)
            date = eat_deal_detail.end_date - eat_deal_detail.start_date
            eat_deal_data = {
                    'eat_deal_id' : eat_deal_detail.id,
                    'image' : list(eat_deal_detail.restaurant.restaurant_image_set.values('images'))[0],
                    'title' : eat_deal_detail.restaurant.name,
                    'menu' : eat_deal_detail.menu,
                    'menu_info' : eat_deal_detail.menu_info,
                    'restaurant_id' : eat_deal_detail.restaurant.id,
                    'restaurant_info' : eat_deal_detail.restaurant_intro,
                    'start_date' : str(eat_deal_detail.start_date.year) + '-' + 
                            str(eat_deal_detail.start_date.month) + '-' + 
                            str(eat_deal_detail.start_date.day),
                    'end_date' : str(eat_deal_detail.end_date.year) + '-' + 
                            str(eat_deal_detail.end_date.month) + '-' + 
                            str(eat_deal_detail.end_date.day),
                    'price' : int(eat_deal_detail.price),
                    'discount_rate' : eat_deal_detail.discount_rate,
                    'discounted_price' : int(eat_deal_detail.price) - (int(eat_deal_detail.price) * int(eat_deal_detail.discount_rate)/100),
                    'remaining_date' : date.days
                }
            return JsonResponse({'result' : eat_deal_data}, status = 200)
        except Eat_Deal.DoesNotExist:
            return JsonResponse({'result' :'DOES_NOT_EXIST_EAT_DEAL'}, status=404)

class RestaurantEatDealLocationCategoryView(View):
    def get(self, request):
        try:
            city = request.GET.get('city', 13)
            location_states = Location_city.objects.prefetch_related('location_state_set').get(id = city)

            states = [
                {
                    'id' : state['id'],
                    'state' : state['state']
                }
            for state in list(location_states.location_state_set.values())]

            return JsonResponse({'result' : states}, status = 200)
        
        except Location_city.DoesNotExist:
            return JsonResponse({'result' : 'DOES_NOT_EXIST_EAT_DEAL_LOCATION'}, status=404)

class ToplistView(View):
    def get(self, request):
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 20))

        toplists = Top_List.objects.order_by('-create_at')[offset * limit : (offset+1) * limit]
        
        toplist = [{
            "id"          : element.id,
            "image"       : element.image,
            "title"       : element.title,
            "description" : element.description
        } for element in toplists]
        return JsonResponse({"toplists": toplist, "offset" : offset+1}, status = 200)


class ToplistDetailView(View):
    def get(self, request, toplist_id):
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 20))

        top_restaurants = Top_lists_Restaurant.objects.select_related('top_list', 'restaurant').filter(top_list_id = toplist_id)[ offset * limit : (offset+1) * limit]
        
        if top_restaurants.exists():
            toplist = {
                "id"          : toplist_id,
                "title"       : top_restaurants[0].top_list.title,
                "description" : top_restaurants[0].top_list.description,
                "created_at"  : top_restaurants[0].top_list.create_at.strftime('%Y-%m-%d')
            }
            restaurants = [{
                "id"            : element.restaurant.id,
                "name"          : element.restaurant.name,
                "address"       : '{} {} {} {}'.format(element.restaurant.location_city.city, element.restaurant.location_state.state, element.restaurant.location_road.road, element.restaurant.location_detail),
                "image"         : element.restaurant.restaurant_image_set.filter(restaurant_id=element.restaurant_id)[0].images,
                "user_image"    : 'https://s3-ap-northeast-2.amazonaws.com/mp-seoul-image-production/873410_1562147913864', 
                "user_nickname" : element.restaurant.review_set.filter(restaurant_id=element.restaurant_id)[0].user.nick_name,
                "user_review"   : element.restaurant.review_set.filter(restaurant_id=element.restaurant_id)[0].content
            } for element in top_restaurants]

            return JsonResponse({"toplist": toplist, "restaurants": restaurants, "offset":offset+1}, status = 200)
        else:
            return HttpResponse(status = 404)
