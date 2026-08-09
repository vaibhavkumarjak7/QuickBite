from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .managers import ItemManager
from django.utils import timezone
# Create your models here.
class Item(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['user_name','item_price']),
        ]
    
    user_name = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    item_name = models.CharField(max_length=100,db_index=True)
    item_desc = models.TextField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    item_image = models.ImageField(upload_to="item_images/",blank=True,null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)
    
    objects = ItemManager()
    all_objects = models.Manager()
    
    def __str__(self):
        return self.item_name + " : " + str(self.item_price)
    
    def get_absolute_url(self):
        return reverse('Food:index')
    
    def delete(self,using=None,keep_parents=False):
        self.is_deleted=True
        self.deleted_at=timezone.now()
        self.save()
        
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    item = models.ManyToManyField(Item,related_name="orders")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
