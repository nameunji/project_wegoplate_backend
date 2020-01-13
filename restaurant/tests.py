import json

from django.test import TestCase
from django.test import Client
from restaurant.models import(
    Top_List, 
    Topic,
    Topic_Top_list, 
    )

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
    def tearDown(self):
        Topic.objects.all().delete()
        Top_List.objects.all().delete()
        
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