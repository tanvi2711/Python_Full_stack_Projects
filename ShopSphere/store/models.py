from django.db.models import *

# Create your models here.
class CategoryModelClass(Model):
  id=AutoField(primary_key=True)
  name=CharField(max_length=100)

  def __str__(self):
    return self.name

class ProductModelClass(Model):
  id=AutoField(primary_key=True)
  name=CharField(max_length=200)
  price=IntegerField()
  category=ForeignKey(CategoryModelClass,CASCADE,related_name="products")
  image=FileField(upload_to="products/")
  details=CharField(max_length=200)

class UserModelClass(Model):
  id=AutoField(primary_key=True)
  name=CharField(max_length=100)
  email=CharField(max_length=100)
  gender=CharField(max_length=10)
  mobile=CharField(max_length=10)
  address=CharField(max_length=200)
  password=CharField(max_length=100)
class cartModelClass(Model):
  id=AutoField(primary_key=True)
  user=ForeignKey(UserModelClass,CASCADE)
  product=ForeignKey(ProductModelClass,CASCADE,related_name="carts")

class OrderModelClass(Model):
  id=AutoField(primary_key=True)
  user=ForeignKey(UserModelClass,CASCADE)
  product=ForeignKey(ProductModelClass,CASCADE,related_name="orders")
  finalprice=IntegerField()
  orderdate=DateField(auto_now=True)
  paymentmethod=CharField(max_length=50)
  address=CharField(max_length=200)
  orderstatus=CharField(max_length=100)