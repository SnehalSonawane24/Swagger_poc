from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import ItemViewSet, APIViewWithSerialiser, APIViewWithoutSerializer, ItemSimpleViewSet

router = DefaultRouter()
router.register(r'model-viewset', ItemViewSet,)

urlpatterns = [
    path('', include(router.urls)),
    path('api-view-with-serializer/', APIViewWithSerialiser.as_view(), name='example-list'),
    path('api-view-without-serializer/', APIViewWithoutSerializer.as_view(), name='item-list'),
    
    path('api-simple-view/', ItemSimpleViewSet.as_view({'get': 'list', 'post': 'create'}), name="simple-view-list"),
    path('api-simple-view/<int:pk>/', ItemSimpleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="simple-view-detail"),
]
