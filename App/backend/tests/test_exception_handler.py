from rest_framework.exceptions import Throttled, NotAuthenticated, AuthenticationFailed, ValidationError
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.views import exception_handler
from api.exceptions import custom_exception_handler


class TestCustomExceptionHandler(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_throttled_exception(self):
        exc = Throttled(wait=60)
        response = custom_exception_handler(exc, {'request': self.factory.get('/api/user/create_user')})

        self.assertEqual(response.status_code, 429)
        self.assertIn('Przekroczono limit żądań przez użytkownika.', response.data['error'])
        self.assertIn('Pozostały czas do odblokowania:', response.data['error'][1])

    def test_not_authenticated_exception(self):
        exc = NotAuthenticated()
        response = custom_exception_handler(exc, {'request': self.factory.get('/api/user/create_user')})

        self.assertEqual(response.status_code, 403)
        self.assertIn('Brak danych uwierzytelniających.', response.data['error'][0])
        self.assertIn('Zaloguj się na konto aby korzystać z zasobów.', response.data['error'][1])
        self.assertEqual(response.data['code'], 'not_authenticated')

    def test_authentication_failed_exception_refresh(self):
        exc = AuthenticationFailed()
        request = self.factory.get('/api/refresh')
        response = custom_exception_handler(exc, {'request': request})

        self.assertEqual(response.status_code, 401)
        self.assertIn('Dane logowania wygasły.', response.data['error'][0])
        self.assertIn('Zaloguj się ponownie aby korzystać z zasobów.', response.data['error'][1])
        self.assertEqual(response.data['code'], 'refresh_token_failed')

    def test_authentication_failed_exception_access(self):
        exc = AuthenticationFailed()
        request = self.factory.get('/api/user/create_user')
        response = custom_exception_handler(exc, {'request': request})

        self.assertEqual(response.status_code, 403)
        self.assertIn('Nie można potwierdzić uprawnień użytkownika do zasobu.', response.data['error'][0])
        self.assertEqual(response.data['code'], 'access_token_failed')

    def test_fallback_to_default_handler(self):
        exc = ValidationError(detail={'field': ['Invalid input']})
        response = custom_exception_handler(exc, {'request': self.factory.get('/api/user/create_user')})

        default_response = exception_handler(exc, {'request': self.factory.get('/api/user/create_user')})
        self.assertEqual(response.status_code, default_response.status_code)
        self.assertEqual(response.data, default_response.data)
