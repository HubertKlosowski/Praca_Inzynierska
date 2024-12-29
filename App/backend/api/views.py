import os.path
import random
import smtplib
import string
from io import BytesIO

import pandas as pd
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, throttle_classes, authentication_classes, \
    permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api.custom_throttle import MakeSubmissionUserRateThrottle, MakeSubmissionAnonRateThrottle, UpdateUserRateThrottle, \
    CreateUserRateThrottle, DeleteUserRateThrottle, LoginRateThrottle, AdminPanelUserRateThrottle
from api.tokens import generate_verification_token, verify_token
from model.api_keys import save_model_token
from model.model_datasets import predict
from model.model_datasets import preprocess_dataframe, detect_lang
from .models import User, Submission
from .serializer import UserSerializer, SubmissionSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([CreateUserRateThrottle])
def create_user(request):
    # sprawdzenie czy wartości pól są puste
    if any(len(str(el)) == 0 for el in request.data.values()):
        return Response({
            'error': ['Żadne pole nie może być puste.']
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    # jeśli użytkownik już istnieje
    if User.objects.filter(username=request.data['username']).exists():
        return Response({
            'error': ['Użytkownik o podanej nazwie już istnieje.']
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    # jesli email już jest na kogoś innego zarejestrowany
    if User.objects.filter(email=request.data['email']).exists():
        return Response({
            'error': ['Użytkownik o podanym adresie email już istnieje.']
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    # walidacja hasła
    data = request.data.copy()

    try:
        validate_password(data['password'])
    except ValidationError as e:
        return Response({
            'error': e.messages
        }, status=status.HTTP_400_BAD_REQUEST)

    # haszowanie hasła
    data['password'] = make_password(data['password'])
    data['submission_num'] = [10, 30, 100][int(data['usertype'])]

    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()

        if int(data['usertype']) == 2:
            token = generate_verification_token(serializer.data['email'])
            link = f'{settings.SITE_URL}{reverse('verify_user')}?token={token}'

            message = loader.render_to_string(
                'mails/create_account.html',
                context={
                    'title': 'Utworzenie konta',
                    'usertype': int(data['usertype']),
                    'link': link
                }
            )
        else:
            message = loader.render_to_string(
                'mails/create_account.html',
                context={
                    'title': 'Utworzenie konta',
                    'usertype': int(data['usertype'])
                }
            )

        email = EmailMessage(
            subject='Utworzenie konta',
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[serializer.data['email']],
        )
        email.content_subtype = 'html'

        try:
            email.send()
        except smtplib.SMTPException:
            return Response({
                'error': ['Nie udało się wysłać wiadomości potwierdzającej dodanie konto.']
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'user': serializer.data, 'success': 'Dodano użytkownika.'
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# Zwrócenie tylko tokenów
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        if len(username) == 0 or len(password) == 0:
            return Response({
                'error': ['Nie podano nazwy użytkownika/hasła.']
            }, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(username=username).exists():
            return Response({
                'error': ['Próba logowania do nieistniejącego konta.']
            }, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not user.is_verified:
            return Response({
                'error': [
                    f'Użytkownik {username} nie jest zweryfikowany.',
                    'Jeśli konto jest administratorem link weryfikacyjny został wysłany na adres mail.',
                    'W przeciwnym przypadku proszę skontaktować się z administratorem.'
                ]
            }, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(password):
            return Response({
                'error': ['Niepoprawne hasło.']
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        return super().post(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
@throttle_classes([LoginRateThrottle])
def get_user_data(request):
    user_id = request.user.user_id
    if not User.objects.filter(id=user_id).exists():
        return Response({
            'error': ['Użytkownik nie istnieje.']
        }, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(id=user_id)
    user_submissions = SubmissionSerializer(Submission.objects.filter(user=user_id), many=True).data

    return Response({
        'submissions': user_submissions,
        'user': UserSerializer(user).data,
        'success': 'Dane użytkownika'
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
@throttle_classes([DeleteUserRateThrottle])
def delete_user(request):
    username = request.user.username
    if not User.objects.filter(username=username).exists():
        return Response({
            'error': ['Użytkownik nie istnieje.']
        }, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)
    submissions = Submission.objects.filter(user=user.id)
    email = user.email

    for submission in submissions:
        os.remove(submission.content.path)
    submissions.delete()
    user.delete()

    message = loader.render_to_string(
        'mails/delete_account.html',
        context={'title': 'Usunięcie konta'}
    )

    email = EmailMessage(
        subject='Usuniecie konta',
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )
    email.content_subtype = 'html'

    try:
        email.send()
    except smtplib.SMTPException:
        return Response({
            'error': ['Nie udało się wysłać wiadomości potwierdzającej usunięcie konta.']
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'user': UserSerializer(user).data,
        'success': f'Użytkownik o nazwie {user.username} został poprawnie usunięty.'
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
@throttle_classes([UpdateUserRateThrottle])
def update_user(request):
    data = request.data

    if {'username', 'email', 'name', 'password'} in set(data.keys()):
        return Response({
            'error': ['Można tylko zmienić tylko nazwę użytkownika, email, imię i hasło.']
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    if any(len(el) == 0 for el in data.values()):
        return Response({
            'error': ['Conajmniej jedno pole musi być wypełnione.']
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    user_id = request.user.user_id
    if not User.objects.filter(id=user_id).exists():
        return Response({
            'error': ['Użytkownik nie istnieje.']
        }, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(id=user_id)

    if 'password' in data:
        try:
            validate_password(request.data['password'])
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
        data['password'] = make_password(data['password'])

    serializer = UserSerializer(user, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'success': 'Dane użytkownika zostały poprawnie zmienione.'
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'GET'])
@permission_classes([AllowAny])
@authentication_classes([JWTTokenUserAuthentication])
@throttle_classes([AdminPanelUserRateThrottle])
def verify_user(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        email = verify_token(token)

        user = User.objects.get(email=email)
        serializer = UserSerializer(user, data={'is_verified': True}, partial=True)
        if not token:
            return Response({'error': ['Token nie został dostarczony.']}, status=status.HTTP_400_BAD_REQUEST)
        if not email:
            user.delete()
            return Response({'error': ['Link wygasł. Czas ważności wynosi 1h.']}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return render(request, os.path.join('mails', 'verify_account.html'), context={'usertype': serializer.data['usertype']})

    if request.method == 'PATCH':
        username = request.data['username']
        if not User.objects.filter(username=username).exists():
            return Response({
                'error': ['Użytkownik nie istnieje.']
            }, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)
        serializer = UserSerializer(user, data={'is_verified': True}, partial=True)

        if serializer.is_valid():
            serializer.save()

            message = loader.render_to_string(
                'mails/verify_account.html',
                context={
                    'title': 'Weryfikacja konta',
                    'usertype': serializer.data['usertype']
                }
            )

            email = EmailMessage(
                subject='Weryfikacja konta',
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[serializer.data['email']],
            )
            email.content_subtype = 'html'

            try:
                email.send()
            except smtplib.SMTPException:
                return Response({
                    'error': ['Nie udało się wysłać wiadomości potwierdzającej weryfikację konta.']
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'success': 'Weryfikacja użytkownika powiodła się.'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
@throttle_classes([AdminPanelUserRateThrottle])
def renew_submission(request):
    username = request.data['username']
    if not User.objects.filter(username=username).exists():
        return Response({
            'error': ['Użytkownik nie istnieje.']
        }, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)
    submission_num = [10, 30, 100][user.usertype]
    serializer = UserSerializer(user, data={'submission_num': submission_num}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': 'Odnowienie prób użytkownika powiodło się.'
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([AllowAny])  # pozwala na wykonanie requesta dla użytkowników jak i anonów
@throttle_classes([MakeSubmissionUserRateThrottle, MakeSubmissionAnonRateThrottle])
def make_submission(request):
    data = request.data.copy()

    # Pola text muszą być w request
    if 'content' not in data.keys():
        return Response({
            'error': ['Pola \"content\" musi być podane.']
        }, status=status.HTTP_400_BAD_REQUEST)

    time_start = timezone.now()

    if request.FILES:
        file_size = request.FILES['content'].size

        if request.user.username == '' and file_size >= 1e4:
            return Response({
                'error': [f'Rozmiar przekazanego pliku przekroczył dopuszczalny limit: {file_size // 1000}KB > 10KB']
            }, status=status.HTTP_400_BAD_REQUEST)

        extension = request.FILES['content'].name.split('.')[-1]

        if extension != 'csv' and extension != 'json':
            return Response({
                'error': ['Plik musi być w rozszerzeniu csv lub json.']
            }, status=status.HTTP_400_BAD_REQUEST)

        # BARDZO WAŻNE !!!!!!!!!!!!!!!!!!!!!!
        my_file = request.FILES['content'].file
        my_file.seek(0)

        df = pd.read_csv(my_file, delimiter='|', index_col=False) if extension == 'csv' else pd.read_json(my_file)

        if 'text' not in df.columns.tolist():
            return Response({
                'error': ['Plik musi zawierać kolumnę \"text\".']
            }, status=status.HTTP_400_BAD_REQUEST)

    else:
        df = pd.DataFrame(data={'text': [data['content']]})

    lang = detect_lang(df)

    if lang != 'en':
        return Response({
            'error': ['Wykryty język nie jest obsługiwany. Podaj dane w języku angielskim.']
        }, status=status.HTTP_400_BAD_REQUEST)

    model = data['model']
    # path = f'D:/{model}'

    if request.user.username == '' and model == 'bert-large':
        return Response({
            'error': ['Bez konta nie można korzystać z modelu LARGE.']
        }, status=status.HTTP_400_BAD_REQUEST)

    path = f'depression-detect/{model}'
    prepared = preprocess_dataframe(df.copy(deep=True), lang=lang)

    try:
        stats = predict(path, prepared, truncate=False, login_token=save_model_token)
        data['time_taken'] = (timezone.now() - time_start).total_seconds()
    except Exception as e:
        return Response({
            'error': [f'{str(e)}']
        }, status=status.HTTP_404_NOT_FOUND)

    concated = pd.concat([df, stats], axis=1)
    buffer = BytesIO()
    concated.to_csv(buffer, index=False)
    buffer.seek(0)
    filename = ''.join(random.choices(string.ascii_letters, k=25))
    filename = f'{filename}.csv'

    result_file = File(buffer, name=filename)

    if request.user.username != '':
        username = request.user.username
        if not User.objects.filter(username=username).exists():
            return Response({
                'error': ['Użytkownik nie istnieje.']
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        user = User.objects.get(username=username)

        if request.FILES:
            file_size = request.FILES['content'].size

            if user.usertype == 0 and file_size >= 2e4:
                return Response({
                    'error': [f'Rozmiar przekazanego pliku przekroczył dopuszczalny limit: {file_size // 1000} > 20KB']
                }, status=status.HTTP_400_BAD_REQUEST)
            elif user.usertype == 1 and file_size >= 1e5:
                return Response({
                    'error': [f'Rozmiar przekazanego pliku przekroczył dopuszczalny limit: {file_size // 1000} > 100KB']
                }, status=status.HTTP_400_BAD_REQUEST)
            elif user.usertype == 2 and file_size >= 1e6:
                return Response({
                    'error': [f'Rozmiar przekazanego pliku przekroczył dopuszczalny limit: {file_size // 1000} > 1MB']
                }, status=status.HTTP_400_BAD_REQUEST)

        data['content'] = result_file

        if user.submission_num == 0:
            return Response({
                'error': ['Użytkownik nie posiada wolnych prób.']
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        user.submission_num -= 1
        user.last_submission = timezone.now()
        user.save()

        serializer = SubmissionSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({
            'success': 'Poprawnie przeprowadzono obliczenia.',
            'depressed': stats['depressed'],
            'text': df['text'],
            'submission': serializer.data
        }, status=status.HTTP_201_CREATED)

    data.pop('content', None)

    return Response({
        'success': 'Poprawnie przeprowadzono obliczenia.',
        'depressed': stats['depressed'],
        'text': df['text']
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
def get_submission(request, sub_uuid):
    submission = Submission.objects.get(id=sub_uuid)

    try:
        results = pd.read_csv(submission.content.path)
    except FileNotFoundError:
        return Response({
            'error': [f'Plik z wskazanej próby nie istnieje.']
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'success': 'Poprawnie odczytano dane.',
        'depressed': results['depressed'],
        'text': results['text'],
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
def change_name(request, sub_uuid):
    submission = Submission.objects.get(id=sub_uuid)

    serializer = SubmissionSerializer(submission, data=request.data, partial=True)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response({
        'success': 'Poprawnie ustawiono nazwę próby.',
        'submission': serializer.data
    }, status=status.HTTP_200_OK)