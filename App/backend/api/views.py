from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .serializer import UserSerializer
import datetime


@api_view(['GET'])
def get_user(request):
    if not User.objects.filter(**request.GET.dict()).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(**request.GET.dict())
    return Response(UserSerializer(user).data)

@api_view(['POST'])
def create_user(request):
    # jesli użytkownik juz istnieje
    if User.objects.filter(username=request.data['username']).exists():
        return Response(data={'error': 'BŁĄD!! Użytkownik o podanej nazwie już istnieje!!'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    # jesli email juz jest na kogos innego zarejestrowany
    if User.objects.filter(email=request.data['email']).exists():
        return Response(data={'error': 'BŁĄD!! Użytkownik o podanym adresie email już istnieje!!'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    # walidacja hasła
    data = request.data.copy()
    try:
        validate_password(data['password'])
    except ValidationError as e:
        return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    # haszowanie hasła
    data['password'] = make_password(data['password'])
    data['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def login(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    if len(username) == 0 or len(password) == 0:
        return Response(data={'error': 'BŁĄD!! Żadne pole nie może być puste!!'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    if not User.objects.filter(username=username).exists():
        return Response(data={'error': 'BŁĄD!! Użytkownik o podanej nazwie nie istnieje!!'},
                        status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)
    if check_password(password, user.password):
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    return Response(data={'error': 'BŁĄD!! Niepoprawne hasło!!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, username):
    if not User.objects.filter(username=username).exists():
        return Response(data={'error': 'BŁĄD!! Użytkownik o podanej nazwie nie istnieje!!'},
                        status=status.HTTP_404_NOT_FOUND)

    User.objects.get(username=username).delete()
    return Response(data={'success': 'Użytkownik został poprawnie usunięty!'},
                    status=status.HTTP_204_NO_CONTENT)