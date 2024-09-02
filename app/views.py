from django.shortcuts import render
from rest_framework import viewsets
from app.models import Item
from app.serializers import ExampleSerialiser, ItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# ModelViewSet with ModelSerializer
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
# APIView with seializers    
# class ExampleAPIView(APIView):
#     def get(self, request, *args, **kargs):
#         item = Item.objects.all()
#         serializer = ExampleSerialiser(item, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = ExampleSerialiser(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ExampleAPIView(APIView):
    @swagger_auto_schema(request_body=ExampleSerialiser)
    def post(self, request, format=None):
        serializer = ExampleSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        item = Item.objects.all()
        serializer = ExampleSerialiser(item, many=True)
        return Response(serializer.data)    
    
    
# APIView without serializer    
# class ExampleAPIViewWithoutSerializer(APIView):
#     def get(self, request, format=None):
#         items = Item.objects.all()
#         data = [{"id": item.id, "name": item.name, "description": item.description} for item in items]
#         return Response(data)

#     def post(self, request, format=None):
#         name = request.data.get("name")
#         description = request.data.get("description")

#         if not name or not description:
#             return Response({"error": "Name and description are required."}, status=status.HTTP_400_BAD_REQUEST)

#         item = Item.objects.create(name=name, description=description)
#         data = {"id": item.id, "name": item.name, "description": item.description}
#         return Response(data, status=status.HTTP_201_CREATED)

class ExampleAPIViewWithoutSerializer(APIView):

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
