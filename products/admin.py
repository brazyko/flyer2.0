from django.contrib import admin
from .models import Product,Category,ProductImage,CommentProduct
from mptt.admin import MPTTModelAdmin,DraggableMPTTAdmin
# Register your models here.

class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    # specify pixel amount for this ModelAdmin only:
    prepopulated_fields={'slug':('name',)}
    mptt_level_indent = 50

admin.site.register(Category,CustomMPTTModelAdmin)

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    max_num = 5
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline]
    list_display = ["title","category","price","views"]

admin.site.register(ProductImage)
admin.site.register(Product, ProductAdmin)
admin.site.register(CommentProduct)