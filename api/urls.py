
from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import MovieViewSet, ratingViewSet, UserViewSet


router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('movies', MovieViewSet)
router.register('ratings', ratingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
