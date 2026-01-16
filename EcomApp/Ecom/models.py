from django.db.models import *

# Create your models here.
class Category(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
class Product(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    price = FloatField()
    category = ForeignKey(Category, on_delete=CASCADE)
    image = ImageField(upload_to='product_images/')
    description = TextField()
