from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('users', views.get_all, name="post_get_users"),
    path('users/<int:pk>', views.get_user, name="get_user_or_update_user"),
]
