from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'accordions', views.AccordionViewSet, base_name='accordions')


urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^$', views.api_root),
    #url(r'^accordion/$', views.AccordionList.as_view(), name='accordion-list'),
    #url(r'^accordion/(?P<pk>[0-9]+)/$', views.AccordionDetail.as_view(), name='accordion-detail'),
]
