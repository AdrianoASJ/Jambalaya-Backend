from rest_framework import serializers
from .models import *


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        depth = 1
        fields = ('id', 'name', 'email', 'city', 'cellphone')


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        depth = 1
        fields = '__all__'

