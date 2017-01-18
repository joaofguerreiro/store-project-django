from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Pastebin API')

router = DefaultRouter()
router.register(r'accordions', views.AccordionViewSet, base_name='accordions')


urlpatterns = [
    url(r'^', include(router.urls)),
    url('^schema/$', schema_view),
]

