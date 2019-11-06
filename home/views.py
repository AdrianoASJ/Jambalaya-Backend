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
        print(e)
        return Response({'status': 300, 'message': 'Erro ao cadastrar verifique os campos preenchidos', 'error': e})


@api_view(['POST'])
@permission_classes([AllowAny])
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

        compare = requests.get(
            'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=1500&type=hotel&keyword=cruise&key=AIzaSyADfFDApH-HJrbmaXnerTiJPK2ZCLA6BU0')

        new_result = result.json()

        return Response({"status": 200, "success": True, "message": "Retornando todos Hoteis", "return": new_result})
    except Exception as e:
        return Response({"status": 300, "success": False, "message": "place_search erro", 'error': e})


@api_view(['POST'])
@permission_classes([AllowAny])
def photo_return(request):
    try:
        key = "AIzaSyADfFDApH-HJrbmaXnerTiJPK2ZCLA6BU0"

        maxwidth = "400"  # tamanho da foto a ser retornada
        photoreference = request.data.get("photoreference")

        result = requests.get(
            'https://maps.googleapis.com/maps/api/place/photo?maxwidth=' + maxwidth + '&photoreference=' + photoreference + '&key=' + key + '')

        compare = requests.get(
            'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=CmRaAAAAnYSxXLPKKumBoU5oARtqBubbUIToDpNfm-tWPCc9TCmnkgDaO93eAljes_2tQq7fxyIPMuOvmne00AqvOOD6wcOUH_qh6f3s6yS1RIvjXV047heIgr7FSY5I1lMQlc8WEhDPjrOjQhH3UJam3kw9sQaoGhQIjCSntQlPm3Q-vWenl1CWkZaVfQ&key=AIzaSyADfFDApH-HJrbmaXnerTiJPK2ZCLA6BU0')

        new_result = result.url

        return Response(
            {"status": 200, "success": True, "message": "Retornando foto de estabelecimento", "return_url": new_result})
    except Exception as e:
        return Response({"status": 300, "success": False, "message": "photo_return erro", 'error': e})


@api_view(['POST'])
@permission_classes([AllowAny])
def reserve(request):
    try:
        account_id = request.data.get("account_id")
        establishment_name = request.data.get("establishment_name")
        childrens = request.data.get("childrens")
        adults = request.data.get("adults")
        babies = request.data.get("babies")
        checkin = request.data.get("checkin")
        checkout = request.data.get("checkout")

        if Account.objects.filter(pk=account_id).count() == 0:
            return Response({"status": 500, "message": "Este usuario nao esta cadastrado em nosso banco de dados", "Conta": None})

        user = Account.objects.get(pk=account_id)

        new_hotel = Hotel()
        new_hotel.user = user
        new_hotel.name = establishment_name
        new_hotel.qtd_criancas = childrens
        new_hotel.qtd_adultos = adults
        new_hotel.qtd_bebes = babies
        new_hotel.checkin = checkin
        new_hotel.checkout = checkout

        new_hotel.save()
        return Response(
            {"status": 200, "success": True, "message": "Reserva concedida"})
    except Exception as e:
        return Response({"status": 300, "success": False, "message": "reserve erro", 'error': e})

@api_view(['POST'])
@permission_classes([AllowAny])
def user_reservation(request):
    try:
        account_id = request.data.get("account_id")

        user = Account.objects.get(pk=account_id)

        hotels = HotelSerializer(Hotel.objects.filter(user__pk=account_id), many=True).data

        return Response({"status": 200, "success": True, "message": "Retornando todos hoteis reservados pelo usuario",
                         "user_hotels": hotels})
    except Exception as e:
        return Response({"status": 300, "success": False, "message": "user_reserves erro", 'error': e})

@api_view(['POST'])
@permission_classes([AllowAny])
def details_place(request):
    try:
        place_id = request.data.get("place_id")
        key = "AIzaSyADfFDApH-HJrbmaXnerTiJPK2ZCLA6BU0"
        fields = 'name,rating,formatted_address,formatted_phone_number,photos,reviews,user_ratings_total'

        result = requests.get('https://maps.googleapis.com/maps/api/place/details/json?place_id=' + place_id + '&fields=' + fields + '&key=' + key + '')

        # compare = request.get('https://maps.googleapis.com/maps/api/place/details/json?key=AIzaSyADfFDApH-HJrbmaXnerTiJPK2ZCLA6BU0&fields=name,rating,formatted_address,formatted_phone_number,photos,reviews,user_ratings_total&place_id=ChIJmXIDXatJxwcRrgUPNSjikyQ')
        new_result = result.json()

        valor = 0
        return Response({"status": 200, "success": True, "message": "Retornando todos detalhes do Hotel",
                            "details": new_result, "price": valor})
    except Exception as e:
        return Response({"status": 300, "success": False, "message": "user_reserves erro", 'error': e})
