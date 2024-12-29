import time

from rest_framework import status
from rest_framework.exceptions import Throttled, AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, Throttled):
        format_time = time.strftime('%H:%M:%S', time.gmtime(exc.wait))
        response_data = {
            'error': ['Przekroczono limit żądań przez użytkownika.', f'Pozostały czas do odblokowania: {format_time}'],
        }
        return Response(response_data, status=status.HTTP_429_TOO_MANY_REQUESTS)

    elif isinstance(exc, NotAuthenticated):
        response_data = {
            'error': ['Brak danych uwierzytelniających.'],
            'code': 'not_authenticated'
        }
        return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    elif isinstance(exc, AuthenticationFailed):
        method = context['request'].get_full_path().split('/')[-1]

        if method == 'refresh':
            response_data = {
                'error': ['Dane logowania wygasły.', 'Zaloguj się ponownie aby korzystać z zasobów.'],
                'code': 'refresh_token_failed'
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        else:
            response_data = {
                'error': ['Nie można potwierdzić uprawnień użytkownika do zasobu.'],
                'code': 'access_token_failed'
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    return exception_handler(exc, context)
