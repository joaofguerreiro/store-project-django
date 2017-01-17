from rest_framework import serializers
from store.models import Accordion


class AccordionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:accordions-detail")

    class Meta:
        model = Accordion
        fields = ('url', 'id', 'brand', 'model_name', 'color', 'price', 'photo',)
