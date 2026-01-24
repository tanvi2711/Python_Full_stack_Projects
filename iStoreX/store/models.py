from django.db import models
from django.conf import settings

class CategoryModelClass(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class ProductModelClass(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="uploads/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(CategoryModelClass, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class CartModelClass(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        ProductModelClass,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user} - {self.product.name}"