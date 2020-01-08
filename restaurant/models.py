from django.db import models


class Restaurant(models.Model):
    name            = models.CharField(max_length=300)
    price_range     = models.ForeignKey('Price', on_delete=models.SET_NULL, null=True)
    food            = models.ForeignKey('Food', on_delete=models.SET_NULL, null=True)
    location_do     = models.ForeignKey('Location_city', on_delete=models.SET_NULL, null=True)
    location_gu     = models.ForeignKey('Location_state', on_delete=models.SET_NULL, null=True)
    location_dong   = models.ForeignKey('Location_road', on_delete=models.SET_NULL, null=True)
    location_detail = models.CharField(max_length=300)

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
