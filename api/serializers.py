from rest_framework.serializers import ModelSerializer
from products.models import Product,Category,ProductImage
from dialogs.models import Message,VoiceMessage,Chat
from map.models import Repairman
from django.contrib.auth.models import User

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','author','title','slug','category','description','summary','features','price','publish','views','users_like','odd_images']

class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug','parent']

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','image','product']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class RepairmanSerializer(ModelSerializer):
    class Meta:
        model = Repairman
        fields = ['id','worksop_name','slug','workshop_image','user','about_workshop','services','coord_v','coord_h']

class MessagesSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['chat','author','message','pub_date','is_readed']
        
class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ['members']
