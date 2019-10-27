from django.contrib.auth.hashers import PBKDF2PasswordHasher
from .models import *
from .serializer import *
import requests
import json

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    try:
        name = request.data.get("nome")
        email = request.data.get("email")
        cellphone = request.data.get("telefone")
        city = request.data.get("cidade")
        password = request.data.get("senha")

        password_encrypting = PBKDF2PasswordHasher()
        password_encrypted = password_encrypting.encode(password, 'seasalt2')

        if Account.objects.filter(email=email).count() >= 1:
            return Response({'status': 800, 'success': False, 'message': 'Já existe um usuário com esse email'})

        conta = Account()

        conta.name = name
        conta.username = email
        conta.email = email
        conta.cellphone = cellphone
        conta.city = city
        conta.password = password_encrypted

        conta.save()

        feedback = AccountSerializer(Account.objects.filter(email=email), many=True).data

        return Response({'status': 200, 'message': 'Conta criada com sucesso', "conta": feedback})
    except Exception as e:
        return Response({'status': 300, 'message': 'Erro ao cadastrar verifique os campos preenchidos', 'error': e})


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def login(request):
    try:
        email = request.data.get("email")
        password = request.data.get("senha")

        if Account.objects.filter(email=email).count() == 0:
            return Response({"status": 500, "message": "Este email não esta cadastrado", "Conta": None})

        conta = Account.objects.get(email=email)

        valid = check_password(password, conta.password)

        if not valid:
            return Response({"status": 600, "success": False, "message": "Senha Invalida", "Conta": None})

        feedback = AccountSerializer(Account.objects.filter(email=email), many=True).data

        return Response({"status": 200, "success": True, "message": "Login efetuado", "Conta": feedback})
    except Exception as e:
        return Response({"status": 300, "success": False, "message": "Login erro", "Conta": None, 'error': e})


@api_view(['GET'])
@permission_classes([AllowAny])
def search_hotels(request):
    try:

        feedback = HotelSerializer(Hotel.objects.all(), many=True).data

        return Response({"status": 200, "success": True, "message": "Retornando todos Hoteis", "Conta": feedback})
    except Exception as e:
        return Response({"status": 300, "success": False, "message": "search_hotels erro", 'error': e})


@api_view(['POST'])
@permission_classes([AllowAny])
def place_search(request):
    try:
        key = "AIzaSyADfFDApH-HJrbmaXnerTiJPK2ZCLA6BU0"

        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        radius = "1500"
        type = "hotel"
        keyword = ""

        result = requests.get(
            'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + latitude + ',' + longitude + '&radius=' + radius + '&type=' + type + '&keyword=' + keyword + '&key=' + key + '')

        compare = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=1500&type=hotel&keyword=cruise&key=AIzaSyADfFDApH-HJrbmaXnerTiJPK2ZCLA6BU0')

        new_result = result.json()

        return Response({"status": 200, "success": True, "message": "Retornando todos Hoteis", "return": new_result})
    except Exception as e:
        return Response({"status": 300, "success": False, "message": "place_search erro", 'error': e})
