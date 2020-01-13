import json

from django.http  import JsonResponse
from django.views import View
from .models import Topic, Topic_Top_list

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