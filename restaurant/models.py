from django.db import models


class Restaurant(models.Model):
    name                    = models.CharField(max_length=300)
    price_range             = models.ForeignKey('Price', on_delete=models.SET_NULL, null=True)
    food                    = models.ForeignKey('Food', on_delete=models.SET_NULL, null=True)
    location_city           = models.ForeignKey('Location_city', on_delete=models.SET_NULL, null=True)
    location_state          = models.ForeignKey('Location_state', on_delete=models.SET_NULL, null=True)
    location_road           = models.ForeignKey('Location_road', on_delete=models.SET_NULL, null=True)
    location_detail         = models.CharField(max_length=300)
    holiday                 = models.ForeignKey('Holiday', on_delete=models.SET_NULL, null=True)
    tags_restaurants        = models.ManyToManyField('Tag', through='Restaurant_Tag')
    restaurants_top_lists   = models.ManyToManyField('Top_List', through='Top_lists_Restaurant')

    class Meta:
        db_table = 'restaurants'

class Price(models.Model):
    price_range     = models.CharField(max_length=200)

    class Meta:
        db_table = 'prices'

class Food(models.Model):
    category        = models.CharField(max_length=200)

    class Meta:
        db_table = 'foods'

class Location_city(models.Model):
    city            = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'location_cities'

class Location_state(models.Model):
    state           = models.CharField(max_length=200)
    city            = models.ForeignKey('Location_city', on_delete=models.SET_NULL, null=True)
        
    class Meta:
        db_table = 'location_states'

class Location_road(models.Model):
    road            = models.CharField(max_length=200)
    state           = models.ForeignKey('Location_state', on_delete=models.SET_NULL, null=True)
        
    class Meta:
        db_table = 'location_roads'

class Restaurant_Info(models.Model):
    restaurant      = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)
    parking         = models.CharField(max_length=300, null=True)
    number          = models.CharField(max_length=20, null=True)
    last_order      = models.CharField(max_length=45, null=True)
    info            = models.CharField(max_length=1000, null=True)
    site            = models.URLField(max_length=2500, null=True)
    breaktime       = models.CharField(max_length=100, null=True)
    opening_hours   = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'restaurants_info'

class Menu(models.Model):
    restaurant      = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)
    menu            = models.CharField(max_length=300)
    price           = models.CharField(max_length=200)

    class Meta:
        db_table = 'menus'

class Restaurant_image(models.Model):
    restaurant      = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)
    images          = models.URLField(max_length=2500)

    class Meta:
        db_table = 'restaurant_images'

class Holiday(models.Model):
    holiday         = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'holidays'

class Tag(models.Model):
    tag             = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'tags'

class Restaurant_Tag(models.Model):
    tag             = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True)
    restaurant      = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'restaurants_tags'

class Eat_Deal(models.Model):
    restaurant       = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)
    restaurant_intro = models.CharField(max_length=300)
    price            = models.CharField(max_length=100)
    start_date       = models.DateTimeField()
    end_date         = models.DateTimeField()
    discount_rate    = models.IntegerField()
    menu             = models.CharField(max_length=300)
    menu_info        = models.CharField(max_length=1000)
    

    class Meta:
        db_table = 'eat_deals'

class Top_List(models.Model):
    title           = models.CharField(max_length=100)
    description     = models.CharField(max_length=400)
    image           = models.URLField(max_length=2500)
    top_lists_topics = models.ManyToManyField('Topic', through='Topic_Top_list')
    create_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'top_lists'

class Top_lists_Restaurant(models.Model):
    restaurant      = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)
    top_list        = models.ForeignKey('Top_List', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'top_lists_restaurants'

    
class Topic(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        db_table = 'topics'

class Topic_Top_list(models.Model):
    topic = models.ForeignKey('Topic',on_delete=models.SET_NULL, null=True)
    top_list = models.ForeignKey('Top_List',on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'topics_top_lists'

class Topic_Restaurant(models.Model):
    topic       = models.ForeignKey('Topic',on_delete=models.SET_NULL, null=True)
    restaurant  = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'topics_restaurants'
