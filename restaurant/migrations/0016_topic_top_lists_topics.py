# Generated by Django 3.0.1 on 2020-01-11 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0015_topic_topic_restaurant_topic_top_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='top_lists_topics',
            field=models.ManyToManyField(through='restaurant.Topic_Top_list', to='restaurant.Top_List'),
        ),
    ]
