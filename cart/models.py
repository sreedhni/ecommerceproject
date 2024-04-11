from django.db import models
from django.db import models
from ecommerceapp.models import Product
from users.models import User

# Create your models here.
class Cart(models.Model):
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    date_added=models.DateField(auto_now_add=True)
    active=models.BooleanField(default=True)


    def __str__(self):
        return self.products.name

    def sub_total(self):
        return self.quantity*self.products.price


class Order(models.Model):
    status_choices = (('Confirmed', 'Confirmed'), 
                      ('Pending', 'Pending'))
    dstatus_choices = (('Delivered', 'Delivered'), 
                      ('Pending', 'Pending'),
                      ('Out for delivery','Out for delivery'),
                      ("Transisting",'Transisting'))

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    address=models.TextField()
    phone=models.CharField(max_length=100)
    order_status=models.CharField(max_length=30,default='Pending',choices=status_choices)
    delivery_status=models.CharField(max_length=50,default='Pending',choices=dstatus_choices)
    no_of_items=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    mode_of_payment=models.CharField(max_length=50,default="cod")

    def __str__(self):
        self.user.username
    def sub_total(self):
        return self.no_of_items*self.products.price
    
from django.core.validators import MinValueValidator,MaxValueValidator

    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=300)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
