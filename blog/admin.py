from django.contrib import admin
from .models import Article,Category,Like,DisLike,Comment

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields={'slug':('name',)}

admin.site.register(Category,CategoryAdmin)

class AutoSlug(admin.ModelAdmin):
	prepopulated_fields={'slug':('title',)}

admin.site.register(Article,AutoSlug)

admin.site.register(Like)

admin.site.register(DisLike)

admin.site.register(Comment)