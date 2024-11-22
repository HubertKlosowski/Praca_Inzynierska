from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.template import loader
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from .models import User
from .serializer import UserSerializer, SubmissionSerializer
from model.my_model import predict_file, create_dataset
from model.my_datasets import preprocess_dataset

import pandas as pd
import smtplib


@api_view(['GET'])
def get_user(request):
    if not User.objects.filter(**request.GET.dict()).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(**request.GET.dict())
    return Response(UserSerializer(user).data)

@api_view(['POST'])
def create_user(request):
    # sprawdzenie czy wartości pól są puste
    if any(len(str(el)) == 0 for el in request.data.values()):
        return Response(data={'error': 'BŁĄD!! Żadne pole nie może być puste.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # jeśli użytkownik już istnieje
    if User.objects.filter(username=request.data['username']).exists():
        return Response(data={'error': 'BŁĄD!! Użytkownik o podanej nazwie już istnieje.'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    # jesli email już jest na kogoś innego zarejestrowany
    if User.objects.filter(email=request.data['email']).exists():
        return Response(data={'error': 'BŁĄD!! Użytkownik o podanym adresie email już istnieje.'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    # walidacja hasła
    data = request.data.copy()
    try:
        validate_password(data['password'])
    except ValidationError as e:
        return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    # haszowanie hasła
    data['password'] = make_password(data['password'])
    data['created_at'] = timezone.now()

    if data['usertype'] == 2:
        data['is_verified'] = True

    serializer = UserSerializer(data=data)

    if serializer.is_valid():

        serializer.save()

        html_msg = loader.render_to_string(
            'mails/create_account.html',
            context={'title': 'Utworzenie konta'}
        )

        email = EmailMessage(
            subject='Utworzenie konta',
            body=html_msg,
            from_email=settings.EMAIL_HOST_USER,
            to=[serializer.data['email']],
        )
        email.content_subtype = 'html'

        try:
            email.send()
        except smtplib.SMTPException as e:
            return Response(data={'error': 'BŁĄD!! Nie udało się wysłać wiadomości potwierdzającej dodanie konto.'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'user': serializer.data, 'success': 'SUKCES!! Dodano użytkownika.'},
                        status=status.HTTP_201_CREATED)
    return Response(data={'error': 'BŁĄD!! Nie udało się dodać użytkownika.', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def login_user(request):
    username = request.data['username']
    password = request.data['password']

    if len(username) == 0 or len(password) == 0:
        return Response(data={'error': 'BŁĄD!! Żadne pole nie może być puste.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not User.objects.filter(username=username).exists():
        return Response(data={'error': f'BŁĄD!! Użytkownik o nazwie {username} nie istnieje.'},
                        status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)

    if not user.is_verified:
        return Response(data={'error': f'BŁĄD!! Użytkownik o nazwie {username} nie został zweryfikowany. '
                                       f'Proszę skontaktować się z administratorem.'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    if check_password(password, user.password):
        return Response(data={'user': UserSerializer(user).data, 'success': 'SUKCES!! Udało się zalogować.'},
                        status=status.HTTP_200_OK)

    return Response(data={'error': 'BŁĄD!! Niepoprawne hasło.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, username):
    if not User.objects.filter(username=username).exists():
        return Response(data={'error': f'BŁĄD!! Użytkownik o nazwie {username} nie istnieje.'},
                        status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)
    email = user.email
    user.delete()

    html_msg = loader.render_to_string(
        'mails/delete_account.html',
        context={'title': 'Usunięcie konta'}
    )

    email = EmailMessage(
        subject='Usuniecie konta',
        body=html_msg,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )
    email.content_subtype = 'html'

    try:
        email.send()
    except smtplib.SMTPException as e:
        return Response(data={'error': 'BŁĄD!! Nie udało się wysłać wiadomości potwierdzającej usunięcie konta.'},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response(data={'success': f'SUKCES!! Użytkownik o nazwie {username} został poprawnie usunięty.'},
                    status=status.HTTP_200_OK)

@api_view(['PATCH'])
def update_user(request, user_id):
    if not User.objects.filter(id=user_id).exists():
        return Response(data={'error': 'BŁĄD!! Użytkownik nie istnieje.'}, status=status.HTTP_404_NOT_FOUND)

    if {'username', 'email', 'name', 'password'} in set(request.data.keys()):
        return Response(data={'error': 'BŁĄD!! Można tylko zmienić tylko nazwę użytkownika, email, imię i hasło.'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    if any(len(el) == 0 for el in request.data.values()) or len(request.data.keys()) == 0:
        return Response(data={'error': 'BŁĄD!! Żadne pole nie może być puste.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    data = dict(zip(request.data.keys(), request.data.values()))
    user = User.objects.get(id=user_id)

    if 'password' in data:
        try:
            validate_password(request.data['password'])
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        data['password'] = make_password(data['password'])

    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(data={'user': UserSerializer(user).data,
                              'success': 'SUKCES!! Dane użytkownika zostały poprawnie zmienione.'},
                        status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def verify_user(request, username):
    if not User.objects.filter(username=username).exists():
        return Response(data={'error': 'BŁĄD!! Użytkownik nie istnieje.'}, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)

    user.is_verified = True

    serializer = UserSerializer(user, data={'is_verified': user.is_verified}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(data={'user': UserSerializer(user).data,
                              'success': 'SUKCES!! Weryfikacja użytkownika powiodła się.'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def renew_submission(request, username):
    if not User.objects.filter(username=username).exists():
        return Response(data={'error': 'BŁĄD!! Użytkownik nie istnieje.'}, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)

    if user.usertype == 0:
        user.submission_num = 10
    elif user.usertype == 1:
        user.submission_num = 30
    else:
        user.submission_num = 100

    serializer = UserSerializer(user, data={'submission_num': user.submission_num}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(data={'user': UserSerializer(user).data, 'success': 'SUKCES!! Liczba prób została odnowiona.'},
                        status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def make_submission(request):
    serializer = SubmissionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    extension = serializer.data['file'].name.split('.')[-1]

    if not User.objects.filter(id=serializer.data['user']).exists():
        return Response({'error': 'BŁĄD!! Użytkownik nie istnieje.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if extension != 'csv':
        return Response({'error': 'BŁĄD!! Plik musi być w rozszerzeniu .csv.'},
                        status=status.HTTP_400_BAD_REQUEST)

    df = pd.read_csv(serializer.data['file'])
    if ['text', 'label'] != df.columns.tolist():
        return Response({'error': 'BŁĄD!! Plik musi zawierać kolumny \"text\", oraz \"label\".'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(id=request.data['user'])

    if user.submission_num == 0:
        return Response({'error': 'BŁĄD!! Użytkownik nie posiada możliwych prób.'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    user.submission_num -= 1
    user.last_submission = timezone.now()
    user.save()

    df = preprocess_dataset(lang=serializer.data['language'], for_train=False)

    try:
        stats = predict_file(
            f'./model/{serializer.data['llm_model']}/',
            create_dataset(df, split_train_test=False)
        )
    except Exception as e:
        return Response({'error': f'BŁĄD!! {str(e)}'}, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'success': 'SUKCES!! Udało się przesłać dane.',
        'stats': stats,
        'submission': serializer.data
    }, status=status.HTTP_201_CREATED)
