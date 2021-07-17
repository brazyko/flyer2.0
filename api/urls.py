from django.urls import path
from .views import ProductsSerialized, ProductCategorySerialized, ProductImageSerialized,UsersSerialized,RepairmanSerialized,ChatSerializer,MessagesSerializer
from rest_framework import routers

app_name = 'api'
router = routers.DefaultRouter()
router.register('products', ProductsSerialized)
router.register('users', UsersSerialized)
router.register('productcategory', ProductCategorySerialized)
router.register('productimage', ProductImageSerialized)
router.register('repairman',RepairmanSerialized)
router.register('messages',MessagesSerializer)
router.register('chats',ChatSerializer)
urlpatterns = router.urls
