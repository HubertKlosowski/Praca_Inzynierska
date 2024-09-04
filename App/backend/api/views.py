from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .serializer import UserSerializer


@api_view(['GET'])
def get_user(request):
    try:
        user = User.objects.get(**request.GET.dict())
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(UserSerializer(user).data)

@api_view(['POST'])
def create_user(request):
    # jesli użytkownik juz istnieje
    if User.objects.filter(username=request.data['username']).exists():
        return Response(data={'error': 'Użytkownik o podanej nazwie już istnieje!!'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # jesli email juz jest na kogos innego zarejestrowany
    if User.objects.filter(email=request.data['email']).exists():
        return Response(data={'error': 'Użytkownik o podanym adresie email już istnieje!!'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # walidacja hasła
    data = request.data.copy()
    try:
        validate_password(data['password'])
    except ValidationError as e:
        return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    # haszowanie hasła
    data['password'] = make_password(data['password'])
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

    if not User.objects.filter(username=username).exists():
        return Response(data={'error': 'Użytkownik o podanej nazwie nie istnieje!!'}, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)
    if check_password(password, user.password):
        return Response(user, status=status.HTTP_200_OK)
    return Response(data={'error': 'Niepoprawne hasło!!'}, status=status.HTTP_400_BAD_REQUEST)
