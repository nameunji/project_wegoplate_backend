from django.db import models
from restaurant.models import Restaurant

class User(models.Model):
    kakao       = models.IntegerField(null=True)
    facebook    = models.IntegerField(null=True)
    nick_name   = models.CharField(max_length=25, unique=True)
    email       = models.CharField(max_length=50, null=True, unique=True)
    password    = models.CharField(max_length=400, null=True)
    like_user   = models.ManyToManyField(Restaurant, through='User_Like')

    class Meta:
        db_table = 'users'

class User_Like(models.Model):
    user        = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    restaurant  = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'user_likes'

class Review(models.Model):
    user            = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    restaurant      = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    content         = models.TextField()
    review_star     = models.ForeignKey('Review_Star', on_delete=models.SET_NULL, null=True)
    create_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'

class Review_image(models.Model):
    review  = models.ForeignKey('Review', on_delete=models.SET_NULL, null=True)
    image   = models.URLField(max_length=4500, null=True)

    class Meta:
        db_table = 'review_images'

class Review_Star(models.Model):
    star    = models.IntegerField()
    content = models.CharField(max_length=20)

    class Meta:
        db_table = 'review_stars'