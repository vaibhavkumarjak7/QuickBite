from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
class Item(models.Model):
    user_name = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    item_name = models.CharField(max_length=100)
    item_desc = models.TextField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_image = models.CharField(max_length=500,default="https://metropizza.com.au/wp-content/uploads/2023/06/food-placeholder.jpeg")
    
    def __str__(self):
        return self.item_name + " : " + str(self.item_price)
    
    def get_absolute_url(self):
        return reverse('Food:index')
    