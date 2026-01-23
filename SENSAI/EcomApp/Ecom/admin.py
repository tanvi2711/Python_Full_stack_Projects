from django.contrib import admin
from . import models 

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','category','description','image']
admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.Product,ProductAdmin)
