from django.db.models import * 

# Create your models here.
class CategoryModelClass(Model):
    id=AutoField(primary_key=True) 
    name=CharField(max_length=100)

    def __str__(self):
        return self.name
    

class ProductModelClass(Model):
    id=AutoField(primary_key=True) 
    name=CharField(max_length=100)
    image=FileField(upload_to='uploads/')
    price=TextField(max_length=100)
    category=ForeignKey(CategoryModelClass,CASCADE,related_name='Products')
    description=CharField(max_length=300)

    