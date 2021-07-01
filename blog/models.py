from django.db import models
from django.urls import reverse
from PIL import Image
from django.utils.text import slugify
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User

from .utils import generate_unique_slug
from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class Category(models.Model):
    name   = models.CharField(max_length=200)
    slug   = models.SlugField(unique=True)
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='child', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"   

    def __str__(self):  
        return self.name
        

class Article(models.Model):
    author        = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title         = models.CharField(max_length=60)
    slug          = models.SlugField(unique=True)
    categories    = models.ManyToManyField(Category,related_name="posts",)
    description   = models.TextField(blank=True, null=True)
    image         = models.ImageField(default='default_product.jpg', upload_to='blog_pics')
    publish       = models.DateTimeField(auto_now=False,auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    view_count    = models.IntegerField(default=0,editable=True)
    featured      = models.BooleanField()
    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Article, self.title)
        else:  # create
            self.slug = generate_unique_slug(Article, self.title)
        super(Article, self).save(*args, **kwargs)
 
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.slug
    @property
    def get_comments(self):
        return self.comments.all()
    
    def get_cat_list(self):
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]


class Comment(MPTTModel):
    user     = models.ForeignKey(User,on_delete=models.CASCADE)
    publish  = models.DateTimeField(auto_now=True,auto_now_add=False)
    content  = models.TextField()
    post     = models.ForeignKey(Article,related_name='comments',on_delete=models.CASCADE)
    parent   = TreeForeignKey('self',on_delete=models.CASCADE, null=True,blank=True,related_name='children')
    
    class MPTTMeta:
        level_attr = 'mptt_level'

    def __str__(self):
        return '{} : {}'.format(self.user,self.content)

    def get_total_likes(self):
        return self.likes.users.count()

    def get_total_dis_likes(self):
        return self.dis_likes.users.count()

class Like(models.Model):
    ''' like  comment '''

    comment = models.OneToOneField(Comment, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment.content)[:30]

class DisLike(models.Model):
    ''' Dislike  comment '''

    comment = models.OneToOneField(Comment, related_name="dis_likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_comment_dis_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment.content)[:30]