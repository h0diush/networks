from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import GroupViewSet, PostViewSet, UserViewSet

router = DefaultRouter()
router.register(r'v1/posts', PostViewSet, basename='posts')
router.register(r'v1/groups', GroupViewSet, basename='groups')
router.register(r'v1/users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
