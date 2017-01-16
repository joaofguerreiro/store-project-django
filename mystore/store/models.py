from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='store/static', default=None, blank=True)

    def __str__(self):
        return self.brand_name


class Accordion(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=200)
    color = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='accordions/', default=None, blank=True)

    def __str__(self):
        return self.model_name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    order_date = models.DateField(null=True)
    payment_type = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=100, null=True)
    total = models.IntegerField(default=0)

    def add_to_cart(self, accordion_id):
        product = Accordion.objects.get(pk=accordion_id)
        try:
            preexisting_order = ProductCart.objects.get(product_id=product.id, cart=self)
            self.total += preexisting_order.product.price
            preexisting_order.quantity += 1
            preexisting_order.save()

        except ProductCart.DoesNotExist:
            new_order = ProductCart.objects.create(
                product=product,
                cart=self,
                quantity=1
            )
            self.total += new_order.product.price
            new_order.save()
        self.save()

    def remove_from_cart(self, accordion_id):
        product = Accordion.objects.get(pk=accordion_id)
        try:
            preexisting_order = ProductCart.objects.get(product_id=product.id, cart=self)
            self.total -= preexisting_order.product.price
            if preexisting_order.quantity > 1:
                preexisting_order.quantity -= 1
                preexisting_order.save()
            else:
                preexisting_order.delete()

        except ProductCart.DoesNotExist:
            pass
        self.save()


class ProductCart(models.Model):
    product = models.ForeignKey(Accordion)
    cart = models.ForeignKey(Cart)
    quantity = models.IntegerField()


class Order(models.Model):
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(User)
    token = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='PENDING')


class ProductOrder(models.Model):
    product = models.ForeignKey(Accordion)
    order = models.ForeignKey(Order)
    quantity = models.IntegerField()

