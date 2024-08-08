from django.urls import path
from . import views

urlpatterns = [
    path('', views.make_video, name='make_video'),
]