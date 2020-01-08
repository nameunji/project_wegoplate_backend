from django.db import models


class Restaurant(models.Model):
    name            = models.CharField(max_length=300)
    price           = models.ForeignKey(Price, on_delete=models.SET_NULL, null=Ture)
    food            = models.ForeignKey(Food_category, on_delete=models.SET_NULL, null=Ture)
    location_do     = models.ForeignKey(Location_do, on_delete=models.SET_NULL, null=Ture)
    location_gu     = models.ForeignKey(Location_gu, on_delete=models.SET_NULL, null=Ture)
    location_dong   = models.ForeignKey(Location_dong, on_delete=models.SET_NULL, null=Ture)
    location_detail = models.CharField(max_length=300)

    class Meta:
        db_table = 'restaurants'



