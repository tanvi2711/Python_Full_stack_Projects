from django.contrib import admin
from . import models

# Register your models here.
class CategoryModelAdmin(admin.ModelAdmin): 
    list_display=('id','name') 

class ProductModelAdmin(admin.ModelAdmin):
    list_display=('name','price','category')

admin.site.register(models.CategoryModelClass,CategoryModelAdmin)
admin.site.register(models.ProductModelClass,ProductModelAdmin)