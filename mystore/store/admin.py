from django.contrib import admin
from . models import Brand, Accordion, ProductOrder, Cart, ProductCart, Order


class AccordionAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'brand', 'price')


class ProductCartAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'active', 'order_date')


class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'user', 'token', 'status')


admin.site.register(Brand)
admin.site.register(Accordion, AccordionAdmin)
admin.site.register(ProductCart, ProductCartAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(ProductOrder, ProductOrderAdmin)
admin.site.register(Order, OrderAdmin)

