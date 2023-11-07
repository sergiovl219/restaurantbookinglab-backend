from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('userinfo', views.UserInfoView.as_view(), name='userinfo'),
]
