from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from .models import User
from .serializer import UserSerializer, SubmissionFileSerializer, SubmissionChatSerializer
from model.my_model import predict, create_dataset
import datetime
import pandas as pd


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
    data['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
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
def login(request):
    username = request.data['username']
    password = request.data['password']

    if len(username) == 0 or len(password) == 0:
        return Response(data={'error': 'BŁĄD!! Żadne pole nie może być puste.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not User.objects.filter(username=username).exists():
        return Response(data={'error': f'BŁĄD!! Użytkownik o nazwie {username} nie istnieje.'},
                        status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(username=username)

    if check_password(password, user.password):
        return Response(data={'user': UserSerializer(user).data, 'success': 'SUKCES!! Udało się zalogować.'},
                        status=status.HTTP_200_OK)

    return Response(data={'error': 'BŁĄD!! Niepoprawne hasło.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, username):
    if not User.objects.filter(username=username).exists():
        return Response(data={'error': f'BŁĄD!! Użytkownik o nazwie {username} nie istnieje.'},
                        status=status.HTTP_404_NOT_FOUND)

    User.objects.filter(username=username).delete()

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
def send_file(request):
    serializer = SubmissionFileSerializer(data=request.data)
    extension = request.data['file'].name.split('.')[-1]

    if not User.objects.filter(id=request.data['user']).exists():
        return Response({'error': 'BŁĄD!! Użytkownik nie istnieje.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if extension != 'csv':
        return Response({'error': 'BŁĄD!! Plik musi być w rozszerzeniu .csv.'},
                        status=status.HTTP_400_BAD_REQUEST)

    df = pd.read_csv(request.data['file'])
    if ['text', 'label'] != df.columns.tolist():
        return Response({'error': 'BŁĄD!! Plik musi zawierać kolumny \"text\", oraz \"label\".'},
                        status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(id=request.data['user'])

        if user.submission_num == 0:
            return Response({'error': 'BŁĄD!! Użytkownik nie posiada możliwych prób.'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        user.submission_num -= 1
        user.save()

        df.dropna(inplace=True)

        try:
            stats = predict(
                f'./model/saved-{serializer.data['llm_model']}-uncased/',
                f'{serializer.data['llm_model']}-uncased',
                create_dataset(df, split_train_test=False)
            )
        except Exception as e:
            return Response({'error': f'BŁĄD!! {str(e)}'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'success': 'SUKCES!! Udało się przesłać dane.',
            'stats': stats,
            'submission': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_answer(request):
    return Response({'answer': 'Idziemy do przodu.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def save_chat(request):
    serializer = SubmissionChatSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'SUKCES!! Udało się zapisać konwersację.'}, status=status.HTTP_200_OK)

    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)