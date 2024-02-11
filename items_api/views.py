from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from .models import Items
from .serializers import ItemSerializer

class ItemsListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # List all items
    @method_decorator(cache_page(300))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        items = Items.objects.all()
        sku = request.query_params.get('sku')
        name = request.query_params.get('name')
        category = request.query_params.get('category')
        in_stock = request.query_params.get('in_stock')

        # Apply filters if they are present
        if sku:
            items = items.filter(sku=sku)
        if name:
            items = items.filter(name__icontains=name)
        if category:
            items = items.filter(category=category)
        if in_stock is not None:  # Explicit check for None, as it could be False
            items = items.filter(in_stock=in_stock.lower() in ['true', '1', 't'])


        
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create item
    def post(self, request, *args, **kwargs):
        data = {
            "sku": request.data.get('sku'),
            "name": request.data.get('name'),
            "category": request.data.get('category'),
            "tags": request.data.get('tags'),
            "in_stock": request.data.get('in_stock'),
            "quantity": request.data.get('quantity')
        }
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
