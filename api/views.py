from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer,ProductCategorySerializer,ProductImageSerializer,UserSerializer,RepairmanSerializer,ChatSerializer,MessagesSerializer
from products.models import Product,Category,ProductImage
from dialogs.models import Chat, Message
from map.models import Repairman

class ProductsSerialized(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCategorySerialized(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = ProductCategorySerializer

class ProductImageSerialized(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class UsersSerialized(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RepairmanSerialized(ModelViewSet):
    queryset = Repairman.objects.all()
    serializer_class = RepairmanSerializer

class ChatSerializer(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class MessagesSerializer(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessagesSerializer