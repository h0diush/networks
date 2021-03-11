from django.urls import path

from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_post, name='new_post'),
    path('group/', views.group, name='group'),
    path('<int:pk>/like/', views.like, name='like'),
    path('myprofile/<str:username>', views.myprofile, name='myprofile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.profile_follow, name='profile_follow'),
    path('profile/<str:username>/unfollow/', views.profile_unfollow, name='profile_unfollow'),    
    path('<int:pk>/not_like/', views.not_like, name='not_like'),
    path('post/<int:pk>/', views.post_id, name='detail'),
    path('<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('group/<str:slug>/', views.group_id, name='group_detail'),
    path('<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
