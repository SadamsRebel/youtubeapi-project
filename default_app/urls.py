from django.urls import path
from . import views


app_name = 'default_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('liked/', views.liked, name='liked')
]
