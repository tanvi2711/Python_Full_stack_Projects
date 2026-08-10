from django.contrib import admin
from . import models
# Register your models here.

class CategoryModelAdmin(admin.ModelAdmin):
  list_display=['name']
class ProductModelAdmin(admin.ModelAdmin):
  list_display=['name','category','price']
class UserModelAdmin(admin.ModelAdmin):
  list_display=['name','email','mobile','gender','address']

admin.site.register(models.CategoryModelClass,CategoryModelAdmin)
admin.site.register(models.ProductModelClass,ProductModelAdmin)
admin.site.register(models.UserModelClass,UserModelAdmin)