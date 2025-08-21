from django.contrib import admin
from order.models import Cart, CartItem, Order, OrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

@admin.register(Order)
class OrderAdmid(admin.ModelAdmin):
    list_display = ['id', 'user', 'status']

admin.site.register(CartItem)
admin.site.register(OrderItem)
