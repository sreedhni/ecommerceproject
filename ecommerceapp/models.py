from django.db import models
from django.db.models import Avg
from django.conf import settings
from users.models import User

class Contact(models.Model):

    name=models.CharField(max_length=50)
    email=models.EmailField()
    desc=models.TextField(max_length=500)
    phonenumber=models.IntegerField(null=True)
    def __str__(self):
        return self.name
    
class Category(models.Model):
    category=models.CharField(max_length=50)
    def __str__(self):
        return self.category
    

class Product(models.Model):
    product_name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models. CharField(max_length=50,null=True)
    price=models.IntegerField(default=0)
    description=models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to='images/images')
    stock=models.IntegerField(null=True)
    is_sold= models.BooleanField(default=False,null=True)
    created_by = models.ForeignKey(User, related_name='items',on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.product_name
    def average_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg']