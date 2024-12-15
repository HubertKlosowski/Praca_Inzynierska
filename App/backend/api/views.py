import smtplib
from io import BytesIO

import pandas as pd
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template import loader
from django.utils import timezone
from django.core.files import File
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from model.model_datasets import preprocess_dataset, detect_lang
from model.model_datasets import predict
from .models import User, Submission
from .serializer import UserSerializer, SubmissionSerializer
import string
import random
from model.api_keys import save_model_token


@api_view(['POST'])
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
    data['submission_num'] = [10, 30, 100][data['usertype']]

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
        except smtplib.SMTPException:
            return Response({
                'error': ['Nie udało się wysłać wiadomości potwierdzającej dodanie konto.']
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'user': serializer.data, 'success': 'Dodano użytkownika.'
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return Response({
            'error': ['Żadne pole nie może być puste.']
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not User.objects.filter(username=username).exists():
        return Response({
            'error': [f'Użytkownik o nazwie {username} nie istnieje.']
        }, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)

    if not user.is_verified:
        return Response({
            'error': [f'Użytkownik o nazwie {username} nie został zweryfikowany.  Proszę skontaktować się z administratorem.']
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    if check_password(password, user.password):
        user_submissions = SubmissionSerializer(Submission.objects.filter(user=user.id), many=True).data

        return Response({
            'submissions': user_submissions,
            'user': UserSerializer(user).data,
            'success': 'Poprawne logowanie.'
        }, status=status.HTTP_200_OK)

    return Response({
        'error': ['Niepoprawne hasło.']
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, username):
    if not User.objects.filter(username=username).exists():
        return Response({
            'error': [f'Użytkownik o nazwie {username} nie istnieje.']
        }, status=status.HTTP_404_NOT_FOUND)

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
    except smtplib.SMTPException:
        return Response({
            'error': ['Nie udało się wysłać wiadomości potwierdzającej usunięcie konta.']
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'user': UserSerializer(user).data,
        'success': f'Użytkownik o nazwie {username} został poprawnie usunięty.'
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def update_user(request, username):
    if not User.objects.filter(username=username).exists():
        return Response({
            'error': ['Użytkownik nie istnieje.']
        }, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    if {'username', 'email', 'name', 'password'} in set(data.keys()):
        return Response({
            'error': ['Można tylko zmienić tylko nazwę użytkownika, email, imię i hasło.']
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    if all(len(el) == 0 for el in data.values()) or len(data.keys()) == 0:
        return Response({
            'error': ['Żadne pole nie może być puste.']
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    user = User.objects.get(username=username)

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


@api_view(['PATCH'])
def verify_user(request, username):
    if not User.objects.filter(username=username).exists():
        return Response({
            'error': ['Użytkownik nie istnieje.']
        }, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)
    serializer = UserSerializer(user, data={'is_verified': True}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': 'Weryfikacja użytkownika powiodła się.'
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def renew_submission(request, username):
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
            'success': 'Liczba prób została odnowiona.'
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@parser_classes([MultiPartParser])
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

        print(file_size)

        if 'user' not in data.keys() and file_size >= 1e4:
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

    if lang != 'en' and lang != 'pl':
        return Response({
            'error': ['Wykryty język nie jest obsługiwany. Podaj dane w języku polskim lub angielskim.']
        }, status=status.HTTP_400_BAD_REQUEST)

    model = data['pl_model'] if lang == 'pl' else data['en_model']
    # path = f'D:/{model}'

    if 'user' not in data.keys() and (model == 'bert-large' or model == 'roberta-large'):
        return Response({
            'error': ['Bez konta nie można korzystać z modeli LARGE.']
        }, status=status.HTTP_400_BAD_REQUEST)

    path = f'depression-detect/{model}'
    prepared = preprocess_dataset(df.copy(deep=True), lang=lang)

    try:
        stats = predict(path, prepared, truncate=False, login_token=save_model_token)
        data['time_taken'] = (timezone.now() - time_start).total_seconds()
    except Exception as e:
        return Response({
            'error': [f'{str(e)}']
        }, status=status.HTTP_404_NOT_FOUND)

    data.pop('pl_model', None)
    data.pop('en_model', None)
    data['model'] = model

    concated = pd.concat([df, stats], axis=1)
    buffer = BytesIO()
    concated.to_csv(buffer, index=False)
    buffer.seek(0)
    filename = ''.join(random.choices(string.ascii_letters, k=25))
    filename = f'{filename}.csv'

    result_file = File(buffer, name=filename)

    if 'user' in data.keys():
        if not User.objects.filter(id=data['user']).exists():
            return Response({
                'error': ['Użytkownik nie istnieje.']
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        user = User.objects.get(id=data['user'])

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
def get_submission(request, sub_uuid):
    submission = Submission.objects.get(id=sub_uuid)

    try:
        results = pd.read_csv(submission.content.path)
    except FileNotFoundError as e:
        return Response({
            'error': [f'Plik z wskazanej próby nie istnieje.']
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'success': 'Poprawnie odczytano dane.',
        'depressed': results['depressed'],
        'text': results['text'],
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def change_name(request, sub_uuid):
    submission = Submission.objects.get(id=sub_uuid)

    name = request.data['name']

    serializer = SubmissionSerializer(submission, data=request.data, partial=True)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response({
        'success': 'Poprawnie ustawiono nazwę próby.',
        'submission': serializer.data
    }, status=status.HTTP_200_OK)