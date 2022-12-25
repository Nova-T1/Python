from django.urls import re_path as url
from posts import views

urlpatterns = [

    url('', views.post_list),
    url('posts/<int:pk>/', views.post_detail)
]