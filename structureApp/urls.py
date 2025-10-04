from .views import StructureViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r'structures', StructureViewSet, basename='structure')

urlpatterns = [
    path('', include(router.urls)),
]
