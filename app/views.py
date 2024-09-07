from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from app.models import Item
from app.serializers import ExampleSerialiser, ItemSerializer, ExampleOutputSerialiser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


# ModelViewSet with ModelSerializer
# class ItemViewSet(viewsets.ModelViewSet):
    
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Specify fields for filtering
    filterset_fields = ['name', 'description']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'id']
    ordering = ['id']
    
    @swagger_auto_schema(
        operation_description="Get list of items with filtering, searching, and ordering.",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_QUERY, description="Filter by description", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or description", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by name or id", type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
class APIViewWithSerialiser(APIView):
    # Specify fields for filtering
    filterset_fields = ['name', 'description']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'id']
    ordering = ['id']
    
    @swagger_auto_schema(
        operation_description="Get list of items with filtering, searching, and ordering.",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_QUERY, description="Filter by description", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or description", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by name or id", type=openapi.TYPE_STRING)
        ]
    )
    # @swagger_auto_schema(request_body=ExampleSerialiser, responses={201:ExampleOutputSerialiser})
    def post(self, request, format=None):
        serializer = ExampleSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={201:ExampleOutputSerialiser})
    def get(self, request, *args, **kwargs):
        
        item = Item.objects.all()
        serializer = ExampleOutputSerialiser(item, many=True)
        return Response(serializer.data)    
    

class APIViewWithoutSerializer(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the item'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the item'),
            },
            required=['name', 'description'],
        )
    )
    def post(self, request, format=None):
        name = request.data.get("name")
        description = request.data.get("description")

        if not name or not description:
            return Response({"error": "Name and description are required."}, status=status.HTTP_400_BAD_REQUEST)

        item = Item.objects.create(name=name, description=description)
        data = {"id": item.id, "name": item.name, "description": item.description}
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        items = Item.objects.all()
        data = [{"id": item.id, "name": item.name, "description": item.description} for item in items]
        return Response(data)


class ItemSimpleViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for manually handling Item CRUD operations.
    """
    @swagger_auto_schema(responses={201:ExampleOutputSerialiser})
    # List all items (GET)
    def list(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
    # Retrieve a specific item by ID (GET)
    def retrieve(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    
    # Create a new item (POST)
    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Update an existing item (PUT)
    def update(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Partial update of an item (PATCH)
    def partial_update(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete an item (DELETE)
    def destroy(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    