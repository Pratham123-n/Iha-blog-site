# Generated by Django 2.2.10 on 2020-09-18 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_post_blog_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='viewed',
            field=models.IntegerField(default=0),
        ),
    ]
