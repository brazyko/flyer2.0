from django.db import models
from django.urls import reverse
from PIL import Image
from django.utils.text import slugify
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User

from .utils import generate_unique_slug

# Create your models here.
class Product(models.Model):
    author      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title       = models.CharField(max_length=60)
    slug        = models.SlugField(unique=True)
    category    = models.ForeignKey('Category',related_name="products",on_delete=models.CASCADE) 
    description = models.TextField(blank=True, null=True)
    summary     = models.TextField()
    features    = models.BooleanField(default=False)
    price       = models.DecimalField(decimal_places=2,max_digits=10000)
    publish     = models.DateTimeField(auto_now=False,auto_now_add=True,)
    city        = models.CharField(max_length=30)
    views       = models.IntegerField(default=0)
    
    users_like  = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='likes',blank=True)

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Product, self.title)
        else:  # create
            self.slug = generate_unique_slug(Product, self.title)
        super(Product, self).save(*args, **kwargs)
    
    def total_likes(self):
            return self.users_like.count()

    def get_like_url(self):
        return reverse("products:like-toggle",kwargs = {"category_slug":self.category.slug,"prodcut_slug":self.slug})
    

    def get_api_like_url(self):
        return reverse("products:like-api-toggle",kwargs = {"category_slug":self.category.slug,"prodcut_slug":self.slug})

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product-detail",kwargs = {"category_slug":self.category.slug,"prodcut_slug":self.slug})

   
class Category(MPTTModel):
    name   = models.CharField(max_length=200)
    slug   = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to = 'images/%Y/%m/%d/%H/%M/%S/',)
    product = models.ForeignKey('Product',on_delete=models.CASCADE,related_name='odd_images')

    def __str__(self):
        return self.product.title


class CommentProduct(models.Model):
        author      = models.ForeignKey(User,on_delete=models.CASCADE)
        product     = models.ForeignKey(Product, related_name='comments',on_delete=models.CASCADE)
        body        = models.TextField()
        created     = models.DateTimeField(auto_now_add=True)
        updated     = models.DateTimeField(auto_now=True)
        # manually deactivate inappropriate comments from admin site
        active      = models.BooleanField(default=True)
        parent      = models.ForeignKey('self', null=True, blank=True, related_name='replies',on_delete=models.CASCADE)

        class Meta:
            # sort comments in chronological order by default
            ordering = ('created',)

        def __str__(self):
            return 'Comment by {}'.format(self.author)