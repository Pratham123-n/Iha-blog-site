from django.contrib import admin
from blog.models import post
from blog.models import Category,Comment

# Register your models here.
admin.site.register(post)
admin.site.register(Category)
admin.site.register(Comment)