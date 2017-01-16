from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = format_suffix_patterns([
    # /store/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /api/

    # auth_links
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^register/$', views.RegisterFormView.as_view(), name='register'),

    # shopping_links
    url(r'^add/(?P<accordion_id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^remove/(?P<accordion_id>\d+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^cart/checkout/$', views.checkout, name='checkout'),

    # /store/scandalli/
    url(r'^(?P<brand_name>\w+)/$', views.brand_detail, name='brand_detail'),

    # /store/scandalli/extremec/
    url(r'^(?P<brand_name>\w+)/(?P<model_name>\w+)/$', views.accordion_detail, name='accordion_detail'),

]) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

