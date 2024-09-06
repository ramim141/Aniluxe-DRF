from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

   


class Product(models.Model):

    
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    
    sizes = models.ManyToManyField(Size, related_name='products')
    colors = models.ManyToManyField(Color, related_name='products')
    
    brand = models.CharField(max_length=200,null=True,blank=True)
    # rating = models.FloatField(default=0.0)
    rating = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    numReviews = models.IntegerField(null=True,blank=True,default=0)
    countInStock = models.IntegerField(null=True,blank=True,default=0)

    
    
    def __str__(self):
        return self.name +" | "+self.brand +" | " + str(self.price)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    rating =  models.IntegerField(null=True,blank=True,default=0)
    comment = models.TextField(null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Reviewed By {self.user.first_name} {self.user.last_name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_products')
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_products')

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    address = models.TextField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} - {self.user.username} - {self.product.name}'
