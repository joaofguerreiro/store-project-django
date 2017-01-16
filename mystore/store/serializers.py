from rest_framework import serializers
from store.models import Accordion


class AccordionSerializer(serializers.HyperlinkedModelSerializer):
    model_name = serializers.HyperlinkedIdentityField(view_name='accordions-detail')

    class Meta:
        model = Accordion
        ordering = ('brand',)
        fields = ('url', 'id', 'brand', 'color', 'price', 'photo',)


