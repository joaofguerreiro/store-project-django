from django.contrib import admin
from . models import Brand, Accordion, ProductOrder, Cart


class AccordionAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'brand', 'price')


class ProductCartAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'active', 'order_date')


admin.site.register(Brand)

admin.site.register(Accordion, AccordionAdmin)
admin.site.register(ProductOrder, ProductCartAdmin)
admin.site.register(Cart, CartAdmin)
