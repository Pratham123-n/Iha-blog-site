from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
# from blog.views import index,post_details,contact_view,post_form_view,edit_post_form_view
from blog.views import search_view, Postlistview,Contact_form_view,Post_create_view
from blog.views import  post_update_view,specific_cat_list_view
from .import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # path('', index),
    path('', Postlistview.as_view(),name= 'post'),
    path('about/',views.about,name='about'),
    # path('<int:id>',post_details),
    # path('contact',contact_view),
    # path('contact',Contact_form_view.as_view(),name = 'contact'),
    path('contact',views.contact_mail,name="contact1"),
    # path('post',post_form_view),
    path('post',Post_create_view.as_view(),name= 'create-post'),
    path('category/<slug:slug>',specific_cat_list_view ,name = 'cat-page'),
    # path('post/<int:id>',edit_post_form_view),
    path('post/<slug:slug>',post_update_view.as_view(),name= 'edit-post'),
    path('post/<slug:slug>/delete',views.post_delete,name= 'delete-post'),
    path('search',search_view,name='search'),
    # path('<slug:slug>',Postdetailview.as_view(), name= 'detail-page'),
    path('<slug:slug>/',views.post_detail, name= 'detail-page'),
    path('logout/',LogoutView.as_view(template_name= 'account/logout.html'), name='logout'),
    path('user/<username>', views.user_articles, name='user_articles'),
]