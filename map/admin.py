from django.contrib import admin


from .models import Repairman,Services
# Register your models here.
class AutoSlug(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("workshop_name",)}
class RepairmanAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("workshop_name",)}

admin.site.register(Repairman, AutoSlug)
admin.site.register(Services)