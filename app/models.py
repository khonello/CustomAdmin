from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.contrib.contenttypes.models import ContentType

# Create your models here.
COUNTRY = [
    ("uk", "United Kingdom"),
    ("usa", "United States of America"),
    ("russia", "Russia")
]
STATUS = [
    ("rejected", "Rejected"),
    ("pending", "Pending"),
    ("approved", "Approved")
]

class CustomUser(AbstractUser):

    phone_number = models.CharField(max_length= 20)
    message = models.TextField(max_length= 500, null= True, blank= True)
    country = models.CharField(max_length= 100, choices= COUNTRY)
    profile_image = models.ImageField(upload_to= "profile/")

    user_permissions = models.ManyToManyField(
        Permission,
        related_name= "customuser_set"
    )
    groups = models.ManyToManyField(
        Group,
        related_name= "customuser_set"
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    
    name = models.CharField(max_length= 255)
    date_added = models.DateTimeField(auto_now_add= True)
    date_modified = models.DateField(auto_now= True)

    class Meta:
        
        verbose_name = "category"
        verbose_name_plural = "categories"


    def __str__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length= 100)
    price = models.PositiveIntegerField()
    available = models.BooleanField(default= True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name= "products")
    date_added = models.DateTimeField(auto_now_add= True)
    date_modified = models.DateField(auto_now= True)

    class Meta:

        verbose_name = "product"
        verbose_name_plural = "products"
        
        permissions = [
            ("ban_product", "can ban product")
        ]

    def __str__(self):
        return self.name
    

class Sale(models.Model):

    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name= "sales")
    delivered = models.BooleanField(default= False)
    date_added = models.DateField(auto_now_add= True)

    def __str__(self):
        return f"{self.product.name.title()} - Sale"


class Comment(models.Model):

    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE, related_name= "comments")
    message = models.TextField(max_length= 1000)
    status = models.CharField(max_length= 20, choices= STATUS)
    date_added = models.DateTimeField(auto_now_add= True)
    date_modified = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.user.username.title()} - Comment"