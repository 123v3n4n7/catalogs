from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from .models import *


class CatalogSerializer(ModelSerializer):
    class Meta:
        model = Catalog
        fields = '__all__'


class ElementSerializer(ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'