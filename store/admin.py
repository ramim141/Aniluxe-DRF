from django.contrib import admin
from .models import Category, Product, Review, Cart, Wishlist, Order, Size, Color

class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'brand', 'rating', 'numReviews', 'countInStock', 'created_at')
    search_fields = ('name', 'category__name', 'brand')
    list_filter = ('category', 'sizes', 'colors', 'rating')
    filter_horizontal = ('sizes', 'colors')  # Allows easier management of many-to-many fields
    ordering = ('-created_at',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'createdAt')
    search_fields = ('product__name', 'user__username')
    list_filter = ('rating',)
    ordering = ('-createdAt',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'size', 'color')
    search_fields = ('user__username', 'product__name')
    list_filter = ('size', 'color')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__name')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'address', 'status', 'created_at')
    search_fields = ('user__username', 'product__name', 'status')
    list_filter = ('status',)
    ordering = ('-created_at',)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
