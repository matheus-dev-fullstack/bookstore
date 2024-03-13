from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import response
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from order.serializers import OrderSerializer

class OrderViewSet(ModelViewSet):
    
    serializer_class = OrderSerializer
    queryset = Order.objects.add()