from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from . models import Brand, Accordion, Cart, ProductCart, ProductOrder, Order
from . forms import UserForm
from . serializers import AccordionSerializer

from rest_framework import permissions
from rest_framework import viewsets

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


def login_user(request):
    username = ''
    if request.POST:
        # email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            messages.add_message(request, messages.SUCCESS, 'Welcome, %s. Thanks for logging in.'
                                                            % request.session['username'])
            return redirect('/store/')
        else:
            messages.add_message(request, messages.WARNING, 'Your email/password are incorrect. Please try again.')

    context = {'username': username}
    return render(request, 'registration/login.html', context)


def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Thank you for visiting. Please come again.')
    return redirect('/store/login')


class RegisterFormView(View):
    form_class = UserForm
    template_name = 'registration/registration_form.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    # processes a form with data
    def post(self, request):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            user = form.save()

            # logs in after registering the user
            authenticate(email=user.email, password=user.password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Welcome, %s. You have successfully created the account.' % user.username)
            return redirect('/store/')
        else:
            return render(request, self.template_name, {'form': form})


class IndexView(generic.ListView):
    template_name = 'store/index.html'
    context_object_name = 'brands_list'

    def get_queryset(self):
        return Brand.objects.all().order_by('brand_name')


@login_required()
def brand_detail(request, brand_name):
    # Displays all the accordions for each brand
    selected_brand = get_object_or_404(Brand, brand_name=brand_name)
    lst_item = selected_brand.accordion_set.order_by('price')
    return render(request, 'store/brand_detail.html', {'selected_brand': selected_brand, 'lst_item': lst_item})


@login_required()
def accordion_detail(request, model_name, brand_name):
    # Displays the detail of an accordion
    selected_accordion = get_object_or_404(Accordion, model_name=model_name)

    if request.POST:
        # if the purchase button is hit
        return redirect('/store/add')

    return render(request, 'store/accordion_detail.html', {'selected_accordion': selected_accordion})


def add_to_cart(request, accordion_id):
    if request.user.is_authenticated():
        try:
            product = Accordion.objects.get(pk=accordion_id)
        except ObjectDoesNotExist:
            pass
        else:
            try:
                cart = Cart.objects.get(user=request.user)

            except ObjectDoesNotExist:
                cart = Cart.objects.create(
                    user=request.user,
                    active=True,
                )
                cart.save()
            cart.add_to_cart(accordion_id)
            messages.add_message(request, messages.SUCCESS, 'The item was added to your Shopping Cart.')
        return redirect('/store/cart')
    else:
        return redirect('/store/')


def remove_from_cart(request, accordion_id):
    if request.user.is_authenticated():
        try:
            product = Accordion.objects.get(pk=accordion_id)
        except ObjectDoesNotExist:
            pass
        else:
            try:
                cart = Cart.objects.get(user=request.user, active=True)
                cart.remove_from_cart(accordion_id)
                messages.add_message(request, messages.WARNING, 'The item was removed from your Shopping Cart.')
            except:
                pass
        return redirect('/store/cart')
    else:
        return redirect('/store/')


def cart(request):
    if request.user.is_authenticated():
        try:
            cart_obj = Cart.objects.get(user=request.user)

        except ObjectDoesNotExist:
            cart_obj = Cart.objects.create(
                user=request.user,
                active=True,
            )
        cart_products = ProductCart.objects.filter(cart=cart_obj)
        context = {
            'cart': cart_obj,
            'cart_products': cart_products,
        }
        return render(request, 'store/cart.html', context)
    else:
        return redirect('/store/')


def checkout(request):
    if request.user.is_authenticated():
        if request.POST:
            try:

                stripe.api_base = "https://api-tls12.stripe.com"

                if stripe.VERSION in ("1.13.0", "1.14.0", "1.14.1", "1.15.1", "1.16.0", "1.17.0", "1.18.0", "1.19.0"):
                    print "Bindings update required."

                try:
                    stripe.Charge.list()
                    print "TLS 1.2 supported, no action required."
                except stripe.error.APIConnectionError:
                    print "TLS 1.2 is not supported. You will need to upgrade your integration."

                try:
                    # Use Stripe's library to make requests...
                    pass
                except stripe.error.CardError as e:
                    # Since it's a decline, stripe.error.CardError will be caught
                    body = e.json_body
                    err = body['error']

                    print "Status is: %s" % e.http_status
                    print "Type is: %s" % err['type']
                    print "Code is: %s" % err['code']
                    # param is '' in this case
                    print "Param is: %s" % err['param']
                    print "Message is: %s" % err['message']
                except stripe.error.RateLimitError as e:
                    # Too many requests made to the API too quickly
                    pass
                except stripe.error.InvalidRequestError as e:
                    # Invalid parameters were supplied to Stripe's API
                    pass
                except stripe.error.AuthenticationError as e:
                    # Authentication with Stripe's API failed
                    # (maybe you changed API keys recently)
                    pass
                except stripe.error.APIConnectionError as e:
                    # Network communication with Stripe failed
                    pass
                except stripe.error.StripeError as e:
                    # Display a very generic error to the user, and maybe send
                    # yourself an email
                    pass
                except Exception as e:
                    # Something else happened, completely unrelated to Stripe
                    pass

                published_key = settings.STRIPE_PUBLISHABLE_KEY
                cart_obj = Cart.objects.get(user=request.user)
                # products_in_the_cart = ProductCart.objects.filter(cart=cart_obj)

                token = request.POST['stripeToken']
                # Create a charge: this will charge the user's card
                print token
                charge = stripe.Charge.create(
                    amount=cart_obj.total,
                    currency="eur",
                    description="Congratulations, you bought stuff!",
                    source=token,
                )

                """try:
                    charge = stripe.Charge.create(
                        amount=1000,
                        currency="eur",
                        description="Example charge",
                        source=token,
                    )
                except stripe.error.CardError as e:
                    # The card has been declined
                    pass"""
                """
                if charge:
                    order = Order.objects.create(
                        cart=cart_obj,
                        user=request.user,
                        token=token,
                        status='PAID',
                    )
                    order.save()

                    for product_in_the_cart in products_in_the_cart:
                        product_in_order = ProductOrder.objects.create(
                            product=product_in_the_cart.product,
                            order=order,
                            quantity=product_in_the_cart.quantity,
                        )
                        product_in_order.save()

                    products_in_the_cart.delete()
                    cart_obj.total = 0
                    cart_obj.save()
                """
                messages.add_message(request, messages.SUCCESS, 'You successfully bought everything in your Shopping Cart.')
            except ObjectDoesNotExist:
                pass

    return redirect('/store/cart')


class AccordionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Accordion.objects.all()
    serializer_class = AccordionSerializer
    permission_classes = permissions.IsAuthenticatedOrReadOnly

    def perform_create(self, serializer):
        serializer.save()


"""
class AccordionList(generics.ListCreateAPIView):
    queryset = Accordion.objects.all()
    serializer_class = AccordionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AccordionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accordion.objects.all()
    serializer_class = AccordionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
"""

