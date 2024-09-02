from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import ItemViewSet, ExampleAPIView, ExampleAPIViewWithoutSerializer

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('examples/', ExampleAPIView.as_view(), name='example-list'),
    path('ex/', ExampleAPIViewWithoutSerializer.as_view(), name='item-list'),
]
