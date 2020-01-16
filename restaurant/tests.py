import jwt
import json
import bcrypt
import datetime

from django.test       import TestCase
from django.test       import Client
from django.db.models  import Avg
from freezegun         import freeze_time
from django.http       import JsonResponse, HttpResponse

from restaurant.models          import *
from user.models                import User, Review, Review_Star, Review_image
from WegoPlate_backend.settings import SECRET_KEY


class MainTopList(TestCase):
    def setUp(self):
        client = Client()
        
        Topic.objects.create(
            id = 1,
            title = '믿고 보는 맛집 리스트'
        )
        Top_List.objects.create(
            id = 1,
            title = '2020 제주 인기 맛집 TOP 60',
            description = '제주의 인기 맛집만 쏙쏙 골라 모았다!!!',
            image = 'https://mp-seoul-image-production-s3.mangoplate.com/keyword_search/meta/pictures/7zsdxmpu4kauzpk7.jpg'
        )
        Topic_Top_list.objects.create(
            id = 1,
            top_list_id = 1,
            topic_id = 1
        )
        Food.objects.create(
            id = 1,
            category = '한식'
        )
        Location_city.objects.create(
            id = 1,
            city = '서울'
        )
        Location_state.objects.create(
            id = 1,
            state = '은평구'
        )
        Location_road.objects.create(
            id = 1,
            road = '녹번동'
        )
        Holiday.objects.create(
            id = 1,
            holiday = '월'
        )
        Price.objects.create(
            id = 1,
            price_range = '만원 미만'
        )
        Restaurant.objects.create(
            id = 1,
            name              = '테스트 레스토랑',
            price_range_id    = 1,
            food_id           = 1,
            location_city_id  = 1,
            location_state_id = 1,
            location_road_id  = 1,
            location_detail   = '12-1번지',
            holiday_id        = 1
        )
        Restaurant_Info.objects.create(
            id              = 1,
            restaurant_id   = 1,
            parking         = '주차공간없음',
            number          = '02-0000-0000',
            last_order      = '10시',
            info            = 'test',
            site            = 'https://www.google.com',
            breaktime       = None,
            opening_hours   = None
        )
        Menu.objects.create(
            id            = 1,
            restaurant_id = 1,
            menu          = '테스트메뉴1',
            price         = '100원'
        )
        Restaurant_image.objects.create(
            id = 1,
            restaurant_id = 1,
            images        = 'https://mp-seoul-image-production-s3.mangoplate.com/10226_1439659099246'
        )
        Topic_Restaurant.objects.create(
            id = 1,
            topic_id      = 1,
            restaurant_id = 1
        )
        User.objects.create(
            id = 1,
            nick_name = 'test',
            email     = 'test@naver.com',
            password  = bcrypt.hashpw('test1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        Review_Star.objects.create(
            id = 1,
            star    = 5,
            content = 'good' 
        )
        Review.objects.create(
            id = 1,
            user_id = 1,
            restaurant_id = 1,
            content = '맛있습니다',
            review_star_id = 1
        )
        Top_lists_Restaurant.objects.create(
            id = 1,
            restaurant_id = 1,
            top_list_id = 1
        )
 

    def tearDown(self):
        Top_lists_Restaurant.objects.all().delete()
        Topic.objects.all().delete()
        Top_List.objects.all().delete()
        Topic_Top_list.objects.all().delete()
        Topic_Restaurant.objects.all().delete()
        Review.objects.all().delete()
        Review_Star.objects.all().delete()
        User.objects.all().delete()
        Restaurant_image.objects.all().delete()
        Menu.objects.all().delete()
        Restaurant_Info.objects.all().delete()
        Restaurant.objects.all().delete()
        Food.objects.all().delete()
        Location_road.objects.all().delete()
        Location_state.objects.all().delete()
        Location_city.objects.all().delete()
        Holiday.objects.all().delete()
        


    def test_TopTopic(self):
        client = Client()

        response = client.get('/restaurant/topic/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'title' : '믿고 보는 맛집 리스트',
                'top_list' : [
                    {
                        'id' : 1,
                        'title' : '2020 제주 인기 맛집 TOP 60',
                        'description' : '제주의 인기 맛집만 쏙쏙 골라 모았다!!!',
                        'image' : 'https://mp-seoul-image-production-s3.mangoplate.com/keyword_search/meta/pictures/7zsdxmpu4kauzpk7.jpg'
                    }
                ]
            }
        )

    def test_restaurant(self):
        client = Client()
        response = client.get('/restaurant/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'title':'믿고 보는 맛집 리스트',
            'restaurant_list':[{
                'id'    : 1,
                'name'  : '테스트 레스토랑',
                'state' : '은평구',
                'food'  : '한식',
                'image' : 'https://mp-seoul-image-production-s3.mangoplate.com/10226_1439659099246',
                'grade' : 5.0
            }]
        })

    def test_restaurant_not_exists(self):
        client = Client()
        response = client.get('/restaurant/3')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"DOES_NOT_EXIST_TOPIC"})

    def test_restaurant_detail_info(self):
        client = Client()
        response = client.get('/restaurant/1/info')

        result = [
            { "title": "주소", "content": ["서울 은평구 녹번동 12-1번지"]},
            { "title": "음식 종류", "content": ["한식"]},
            { "title": "가격대", "content": ["만원 미만"]},
            { "title": "휴일", "content": ["월"]},
            { "title": "주차", "content": ["주차공간없음"]},
            { "title": "전화번호", "content": ["02-0000-0000"]},
            { "title": "마지막주문", "content": ["10시"]},
            { "title": "웹 사이트", "content": ["https://www.google.com"]},
            { "title": "메뉴", "content": [{"menu":"테스트메뉴1","price":"100원"}]}
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{"result":result})
    
    def test_Restaurant_Detail_Toplist(self):
        client = Client()
        response = client.get('/restaurant/1/toplist')

        toplist = [{
            'id'          : 1,
            'title'       : '2020 제주 인기 맛집 TOP 60',
            'description' : '제주의 인기 맛집만 쏙쏙 골라 모았다!!!',
            'image'       : 'https://mp-seoul-image-production-s3.mangoplate.com/keyword_search/meta/pictures/7zsdxmpu4kauzpk7.jpg'
        }]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result" : toplist})
    
    def test_Restaurant_Detail_Toplist_not_exists(self):
        client = Client()
        response = client.get('/restaurant/2/toplist')

        Restaurant.objects.create(
            id = 2,
            name              = '테스트 레스토랑2',
            price_range_id    = 1,
            food_id           = 1,
            location_city_id  = 1,
            location_state_id = 1,
            location_road_id  = 1,
            location_detail   = '12-1번지',
            holiday_id        = 1
        )

        self.assertEqual(response.status_code, 404)

    def test_Restaurant_Detail_Toplist_Related(self):
        client = Client()
        response = client.get('/restaurant/1/related')

        toplist_title = '2020 제주 인기 맛집 TOP 60'
        restaurant_list = [{
            'id'    : 1,
            'name'  : '테스트 레스토랑',
            'state' : '은평구',
            'food'  : '한식',
            'image' : 'https://mp-seoul-image-production-s3.mangoplate.com/10226_1439659099246',
            'grade' : 5.0
        }]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"title":toplist_title, "restaurant_list":restaurant_list})

    def test_token(self):
        client = Client()

        user = {
            'email'    : 'test@naver.com',
            'password' : 'test1234'
        }
        response = client.post('/user/signin', json.dumps(user), content_type='application/json')
        return response.json()['access_token']

    def test_detail_review_post(self):
        client = Client()
        access_token = self.test_token()

        test = {
	        "restaurant_id":"1",
	        "content":"생각보다 맛있었어요",
	        "star":"good"
        }
        response = client.post('/restaurant/1/review', json.dumps(test), **{'HTTP_AUTHORIZATION':access_token,'content_type' : 'application/json'})

        self.assertEqual(response.status_code, 200)
    


class DetailTopImageBar(TestCase):
    @freeze_time("2012-01-14")
    def setUp(self):
        client = Client()

        Location_city.objects.create(
            id = 1,
            city = '서울시'
        )

        Location_state.objects.create(
            id = 1,
            state = '동작구',
            city_id = 1
        )
        
        Location_road.objects.create(
            id = 1,
            road = '상도로',
            state_id = 1
        )

        Food.objects.create(
            id = 1,
            category = '치킨'
        )

        Price.objects.create(
            id = 1,
            price_range = '1만원'
        )

        Holiday.objects.create(
            id = 1,
            holiday = '일'
        )

        Restaurant.objects.create(
            id = 1,
            name = 'name',
            price_range_id = 1,
            food_id = 1,
            location_city_id = 1,
            location_state_id = 1,
            location_road_id = 1,
            location_detail = '14',
            holiday_id = 1
        )

        Restaurant_image.objects.create(
            id = 1,
            images ='https://mp-seoul-image-production-s3.mangoplate.com/keyword_search/meta/pictures/7zsdxmpu4kauzpk7.jpg',
            restaurant_id = 1
        )

        User.objects.create(
            id = 1,
            nick_name = 'test',
            email     = 'test@naver.com',
            password  = 'test1234'
        )

        Review_Star.objects.create(
            id = 1,
            star = 5,
            content = 'good'
        )

        Review.objects.create(
            id = 1,
            user_id = 1,
            restaurant_id = 1,
            content = 'Hi',
            review_star_id = 1,
            create_at = datetime.datetime.now()
        )

        Review_image.objects.create(
            id = 1,
            image = 'https://mp-seoul-image-production-s3.mangoplate.com/572525_1578455243664775.jpg',
            review_id = 1
        )

        Tag.objects.create(
            id = 1,
            tag = '여기다'
        )

        Restaurant_Tag.objects.create(
            id = 1,
            restaurant_id = 1,
            tag_id = 1
        )
        
        Eat_Deal.objects.create(
            id = 1,
            price = '1000',
            start_date = '2020-01-13',
            end_date = '2020-04-14',
            discount_rate = 15,
            menu = '삼겹살',
            menu_info = '맛있다',
            restaurant_id = 1,
            restaurant_intro = '맛있어'
        )



    def test_detail_top_image(self):
        client = Client()

        response = client.get('/restaurant/1/topimage')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'image' : [
                     'https://mp-seoul-image-production-s3.mangoplate.com/keyword_search/meta/pictures/7zsdxmpu4kauzpk7.jpg'   
                ]     
            }
        )

    def test_detail_review(self):
        client = Client()

        response = client.get('/restaurant/1/review')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'total_count' : 1,
                'good_count' : 1,
                'soso_count' : 0,
                'bad_count' : 0,
                'result' : [
                    {
                        'name' : 'test',
                        'rating' :'good',
                        'text' : 'Hi',
                        'imglist' : ['https://mp-seoul-image-production-s3.mangoplate.com/572525_1578455243664775.jpg'],
                        'time' : '2012-1-14'
                    }
                ]
            }
        )


    def test_detail_near_restaurant(self):
        client = Client()

        response = client.get('/restaurant/1/near')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'result' : [
                    {
                        'id' : 1,
                        'title' : 'name',
                        'food' : '치킨',
                        'price' : '1만원',
                        'location' : '동작구',
                        'img' : {
                            'images' : 'https://mp-seoul-image-production-s3.mangoplate.com/keyword_search/meta/pictures/7zsdxmpu4kauzpk7.jpg'
                        },
                        'avg' : 5.0
                    }
                ]
            }
        )

    def test_detail_near_not_exist_restaurant(self):
        client = Client()

        response = client.get('/restaurant/250/near')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message' : 'DOES_NOT_EXIST_RESTAURANT'
            }
        )
    
    def test_detail_restaurant_tag(self):
        client = Client()

        response = client.get('/restaurant/1/tag')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {

                'result' : 
                [
                    {
                        'id' : 1,
                        'tag' : '여기다' 
                    }
                ]
            }
        )  


    def test_eat_deal(self):
        client = Client()

        response = client.get('/restaurant/eat_deal')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'result' : [
                    {
                        'offset' : 0,
                        'eat_deal_id' : 1,
                        'title' : 'name',
                        'restaurant_id' : 1,
                        'image' : {
                           'images' : 'https://mp-seoul-image-production-s3.mangoplate.com/keyword_search/meta/pictures/7zsdxmpu4kauzpk7.jpg'
                        },
                        'menu' : '삼겹살',
                        'discount_rate' : 15,
                        'price' : 1000,
                        'discounted_price' : 850.0
                    }
                ]
            }
        )

    def teat_eat_deal_search(self):
        client = Client()

        response = client.get('/restaurant/eat_deal?list=1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "result": [
                    {
                        'offset' : 0,
                        'eat_deal_id' : 1,
                        'title' : 'name',
                        'restaurant_id' : 1,
                        'image' : {
                           'images' : 'https://mp-seoul-image-production-s3.mangoplate.com/keyword_search/meta/pictures/7zsdxmpu4kauzpk7.jpg'
                        },
                        'menu' : '삼겹살',
                        'discount_rate' : 15,
                        'price' : 1000,
                        'discounted_price' : 850.0
                    }
                ]
            }
        )

    def tearDown(self):
        Restaurant_image.objects.all().delete()
        Restaurant.objects.all().delete()
        Holiday.objects.all().delete()
        Location_road.objects.all().delete()
        Location_state.objects.all().delete()
        Location_city.objects.all().delete()
        Food.objects.all().delete()
        Price.objects.all().delete()
        Review.objects.all().delete()
        User.objects.all().delete()
        Review_Star.objects.all().delete()
        Review_image.objects.all().delete()
        Eat_Deal.objects.all().delete()


