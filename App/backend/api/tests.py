import os
import uuid
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from rest_framework.test import APIClient

from api import custom_throttle
from api.models import User, Submission
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

custom_throttle.allow_request_for_test()


class TestLoginUser(TestCase):
    def setUp(self):
        self.c = APIClient()
        self.user_verified = User.objects.create(**{
            'username': 'user_verified',
            'email': 'a@a.com',
            'password': make_password('passwd'),
            'name': 'test',
            'is_verified': True,
        })
        self.user_not_verified = User.objects.create(**{
            'username': 'user_not_verified',
            'email': 'a1@a.com',
            'password': make_password('passwd'),
            'name': 'test1',
            'is_verified': False,
        })

    def test_login_user_empty_data(self):
        no_data = self.c.post('/api/user/login_user', data={})
        self.assertEqual(no_data.status_code, 400)
        self.assertEqual(no_data.json()['error'], ['Żadne pole nie może być puste.'])

    def test_login_user_not_verified(self):
        login_not_verified = self.c.post('/api/user/login_user', data={'username': 'user_not_verified', 'password': 'passwd'})
        self.assertEqual(login_not_verified.status_code, 403)

    def test_login_user_not_exists(self):
        login_not_exists = self.c.post('/api/user/login_user', data={'username': 'not', 'password': 'passwd'})
        self.assertEqual(login_not_exists.status_code, 404)

    def test_login_user_bad_passsword(self):
        login_bad_passsword = self.c.post('/api/user/login_user', data={'username': 'user_verified', 'password': 'passwd123'})
        self.assertEqual(login_bad_passsword.status_code, 406)
        self.assertEqual(login_bad_passsword.json()['error'], ['Niepoprawne hasło.'])

    def test_login_user_correct(self):
        login_correct = self.c.post('/api/user/login_user', data={'username': 'user_verified', 'password': 'passwd'})
        self.assertEqual(login_correct.status_code, 200)


class TestCreateUser(TestCase):
    def setUp(self):
        self.c = APIClient()

    def test_create_user_already_exists(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account'
        }
        User.objects.create(**data)
        self.assertEqual(User.objects.count(), 1)
        create_already_exists = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(create_already_exists.status_code, 406)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_empty(self):
        test_create_user_empty = self.c.post('/api/user/create_user', data={})
        self.assertEqual(test_create_user_empty.status_code, 406)

    def test_create_user_with_empty_fields(self):
        create_with_empty_fields = self.c.post('/api/user/create_user', data={
            'name': '',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account'
        })
        self.assertEqual(create_with_empty_fields.status_code, 406)
        self.assertEqual(create_with_empty_fields.json(), ['Żadne pole nie może być puste.'])

    def test_create_user_too_short_password(self):
        create_too_short_password = self.c.post('/api/user/create_user', data={
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'New123!',
            'usertype': -1,
            'username': 'admin_account'
        })
        response_data = create_too_short_password.json()
        self.assertEqual(create_too_short_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Zbyt krótkie hasło (min. 8 znaków).', response_data['error'])

    def test_create_user_too_long_password(self):
        create_too_long_password = self.c.post('/api/user/create_user', data={
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'New123!New123!New123!New123!New123!New123!New123!',
            'usertype': -1,
            'username': 'admin_account'
        })
        response_data = create_too_long_password.json()
        self.assertEqual(create_too_long_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Zbyt długie hasła (max. 32 znaków).', response_data['error'])

    def test_create_user_no_digits_in_password(self):
        create_no_digits_in_password = self.c.post('/api/user/create_user', data={
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'New!New!New!',
            'usertype': -1,
            'username': 'admin_account'
        })
        response_data = create_no_digits_in_password.json()
        self.assertEqual(create_no_digits_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera cyfr.', response_data['error'])

    def test_create_user_no_capital_letters_in_password(self):
        create_no_capital_letters_in_password = self.c.post('/api/user/create_user', data={
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'new123!new123!new123!',
            'usertype': -1,
            'username': 'admin_account'
        })
        response_data = create_no_capital_letters_in_password.json()
        self.assertEqual(create_no_capital_letters_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera dużych liter.', response_data['error'])

    def test_create_user_no_special_characters_in_password(self):
        create_no_special_characters_in_password = self.c.post('/api/user/create_user', data={
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'New123New123New123',
            'usertype': -1,
            'username': 'admin_account'
        })
        response_data = create_no_special_characters_in_password.json()
        self.assertEqual(create_no_special_characters_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera specjalnych znaków.', response_data['error'])

    def test_create_user_wrong_usertype(self):
        create_wrong_usertype = self.c.post('/api/user/create_user', data={
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': -1,
            'username': 'admin_account'
        })
        self.assertEqual(create_wrong_usertype.status_code, 400)

    def test_create_user_wrong_email(self):
        create_wrong_email = self.c.post('/api/user/create_user', data={
            'name': 'Hubert Kłosowski',
            'email': 'ainteria.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account'
        })
        self.assertEqual(create_wrong_email.status_code, 400)

    def test_create_user_correct(self):
        create_correct = self.c.post('/api/user/create_user', data={
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account'
        })
        self.assertEqual(create_correct.status_code, 201)


class TestUpdateUser(TestCase):
    def setUp(self):
        self.c = APIClient()
        self.user = User.objects.create(**{
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account',
            'is_verified': True
        })
        self.token = get_tokens_for_user(user=self.user)['access']

    def test_update_user_only_wrong_field(self):
        changed_data = {'usertype': 0}
        update_only_wrong_field = self.c.patch(
            '/api/user/update_user',
            data=changed_data,
            headers={'Authorization': 'Bearer ' + self.token}
        )
        response_data = update_only_wrong_field.json()
        self.assertEqual(update_only_wrong_field.status_code, 406)
        self.assertEqual(response_data['error'], ['Można tylko zmienić tylko nazwę użytkownika, email, imię i hasło.'])

    def test_update_user_at_least_one_field(self):
        changed_data = {'username': '', 'email': '', 'password': 'newPassowrd123!@#'}
        update_at_least_one_field = self.c.patch(
            '/api/user/update_user',
            data=changed_data,
            headers={'Authorization': 'Bearer ' + self.token}
        )
        response_data = update_at_least_one_field.json()
        self.assertEqual(update_at_least_one_field.status_code, 406)
        self.assertEqual(response_data['error'], ['Żadne pole nie może być puste.'])

    def test_update_user_not_exists(self):
        self.c.delete('/api/user/delete_user', headers={'Authorization': 'Bearer ' + self.token})
        changed_data = {'username': 'admin_account'}
        update_not_exists = self.c.patch(
            '/api/user/update_user',
            data=changed_data,
            headers={'Authorization': 'Bearer ' + self.token}
        )
        response_data = update_not_exists.json()
        self.assertEqual(update_not_exists.status_code, 404)
        self.assertEqual(response_data['error'], ['Użytkownik nie istnieje.'])

    def test_update_user_forbidden(self):
        changed_data = {'username': 'admin_account_2'}
        update_forbidden = self.c.patch('/api/user/update_user', data=changed_data)
        self.assertEqual(update_forbidden.status_code, 403)

    def test_update_user_too_short_password(self):
        changed_data = {'password': 'New123!'}
        update_too_short_password = self.c.patch(
            '/api/user/update_user',
            data=changed_data,
            headers={'Authorization': 'Bearer ' + self.token}
        )
        response_data = update_too_short_password.json()
        self.assertEqual(update_too_short_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Zbyt krótkie hasło (min. 8 znaków).', response_data['error'])

    def test_update_user_too_long_password(self):
        changed_data = {'password': 'New123!New123!New123!New123!New123!New123!New123!'}
        update_too_long_password = self.c.patch(
            '/api/user/update_user',
            data=changed_data,
            headers={'Authorization': 'Bearer ' + self.token}
        )
        response_data = update_too_long_password.json()
        self.assertEqual(update_too_long_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Zbyt długie hasła (max. 32 znaków).', response_data['error'])

    def test_update_user_no_digits_in_password(self):
        changed_data = {'password': 'New!New!New!'}
        update_no_digits_in_password = self.c.patch(
            '/api/user/update_user',
            data=changed_data,
            headers={'Authorization': 'Bearer ' + self.token}
        )
        response_data = update_no_digits_in_password.json()
        self.assertEqual(update_no_digits_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera cyfr.', response_data['error'])

    def test_update_user_no_capital_letters_in_password(self):
        changed_data = {'password': 'new123!new123!new123!'}
        update_no_capital_letters_in_password = self.c.patch(
            '/api/user/update_user',
            data=changed_data,
            headers={'Authorization': 'Bearer ' + self.token}
        )
        response_data = update_no_capital_letters_in_password.json()
        self.assertEqual(update_no_capital_letters_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera dużych liter.', response_data['error'])

    def test_update_user_no_special_characters_in_password(self):
        changed_data = {'password': 'New123New123New123'}
        update_no_special_characters_in_password = self.c.patch(
            '/api/user/update_user',
            data=changed_data,
            headers={'Authorization': 'Bearer ' + self.token}
        )
        response_data = update_no_special_characters_in_password.json()
        self.assertEqual(update_no_special_characters_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera specjalnych znaków.', response_data['error'])

    def test_update_user_correct(self):
        changed_data = {'username': 'admin_account_2'}
        update_correct = self.c.patch(
            '/api/user/update_user',
            data=changed_data,
            headers={'Authorization': 'Bearer ' + self.token}
        )
        self.assertEqual(update_correct.status_code, 200)


class TestDeleteUser(TestCase):
    def setUp(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account',
            'is_verified': True
        }
        self.c = Client()
        self.c.post('/api/user/create_user', data=data)
        login = self.c.post('/api/user/login_user', data=data)
        self.token = login.json()['access']

    def test_delete_user(self):
        self.assertEqual(User.objects.count(), 1)
        delete = self.c.delete('/api/user/delete_user', headers={'Authorization': 'Bearer ' + self.token})
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(delete.status_code, 200)
        delete_again = self.c.delete('/api/user/delete_user', headers={'Authorization': 'Bearer ' + self.token})
        self.assertEqual(delete_again.status_code, 404)

    def test_delete_user_forbidden(self):
        delete_forbidden = self.c.delete('/api/user/delete_user')
        self.assertEqual(delete_forbidden.status_code, 403)


class TestReadUser(TestCase):
    def setUp(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account',
            'is_verified': True
        }
        self.c = Client()
        self.c.post('/api/user/create_user', data=data)
        self.token = self.c.post('/api/user/login_user', data=data).json()['access']

    def test_read_user_forbidden(self):
        read_forbidden = self.c.get('/api/user/get_user_data')
        self.assertEqual(read_forbidden.status_code, 403)

    def test_read_user_not_exists(self):
        self.c.delete('/api/user/delete_user', headers={'Authorization': 'Bearer ' + self.token})
        read_not_exists = self.c.get('/api/user/get_user_data', headers={'Authorization': 'Bearer ' + self.token})
        self.assertEqual(read_not_exists.status_code, 404)

    def test_read_user_correct(self):
        read_correct = self.c.get('/api/user/get_user_data', headers={'Authorization': 'Bearer ' + self.token})
        self.assertEqual(read_correct.status_code, 200)

    def test_read_user_all_users(self):
        read_all_users = self.c.get('/api/get_users', headers={'Authorization': 'Bearer ' + self.token})
        self.assertEqual(read_all_users.status_code, 200)
        self.assertEqual(len(read_all_users.json()), 1)


class TestAdminUser(TestCase):
    def setUp(self):
        admin = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': make_password('Abecadło123!'),
            'usertype': 2,
            'submission_num': 100,
            'username': 'admin_account',
            'is_verified': True
        }
        user = {
            'name': 'Hubert Kłosowski',
            'email': 'a@a.pl',
            'password': make_password('Abecadło123!'),
            'usertype': 1,
            'submission_num': 20,
            'username': 'pro_account',
            'is_verified': False
        }

        self.admin = User.objects.create(**admin)
        self.user = User.objects.create(**user)
        self.c = Client()
        admin['password'] = 'Abecadło123!'
        self.token = self.c.post('/api/user/login_user', data=admin).json()['access']

    def test_renew_submission_forbidden(self):
        admin_forbidden = self.c.patch(
            '/api/user/renew_submission',
            content_type='application/json'
        )
        self.assertEqual(admin_forbidden.status_code, 403)

    def test_renew_submission_correct(self):
        renew_submission = self.c.patch(
            '/api/user/renew_submission',
            data={'username': self.user.username},
            headers={'Authorization': 'Bearer ' + self.token},
            content_type='application/json'
        )
        response_data = renew_submission.json()
        self.assertEqual(renew_submission.status_code, 200)
        self.assertEqual('Odnowienie prób użytkownika powiodło się.', response_data['success'])
        new_user = User.objects.get(username=self.user.username)
        self.assertEqual(new_user.submission_num, 30)

    def test_renew_submission_not_found(self):
        self.user.delete()
        renew_submission = self.c.patch(
            '/api/user/renew_submission',
            data={'username': self.user.username},
            headers={'Authorization': 'Bearer ' + self.token},
            content_type='application/json'
        )
        response_data = renew_submission.json()
        self.assertEqual(renew_submission.status_code, 404)
        self.assertIn('Użytkownik nie istnieje.', response_data['error'])


class VerifyUserTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create(**{
            'name': 'Hubert Kłosowski',
            'email': 'a@a.pl',
            'password': make_password('Abecadło123!'),
            'usertype': 1,
            'submission_num': 20,
            'username': 'pro_account',
            'is_verified': False
        })
        self.token = jwt.encode(
            {'email': self.user.email, 'exp': datetime.now() + timedelta(hours=1)},
            settings.SIMPLE_JWT['SIGNING_KEY'],
            algorithm=settings.SIMPLE_JWT['ALGORITHM']
        )
        self.expired_token = jwt.encode(
            {'email': self.user.email, 'exp': datetime.now() - timedelta(hours=1)},
            settings.SIMPLE_JWT['SIGNING_KEY'],
            algorithm=settings.SIMPLE_JWT['ALGORITHM']
        )
        self.invalid_token = 'invalid.token.value'

    def test_verify_user_no_token_provided(self):
        response = self.c.get('/api/user/verify_user')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Token nie został dostarczony.', response.json()['error'])

    def test_verify_user_invalid_token(self):
        response = self.c.get('/api/user/verify_user', {'token': self.invalid_token})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Weryfikacja się nie powiodła.', response.json()['error'])

    def test_verify_user_expired_token(self):
        response = self.c.get('/api/user/verify_user', {'token': self.expired_token})
        self.assertEqual(response.status_code, 401)
        self.assertEqual('Token wygasł (czas ważności: 1h).', response.json()['error'][1])
        self.assertIn('Weryfikacja się nie powiodła.', response.json()['error'])

    def test_verify_user_valid_token(self):
        response = self.c.get('/api/user/verify_user', {'token': self.token})
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)


class TestAnonSubmission(TestCase):
    def setUp(self):
        self.c = Client()
        self.en = 'I dont want to do this!'

    def test_submission_missing_content(self):
        submission = self.c.post('/api/submission/make_submission', data={'model': 'bert-base'})
        self.assertEqual(submission.status_code, 400)
        self.assertEqual(submission.json()['error'], ['Pola \"content\" musi być podane.'])
        self.assertEqual(Submission.objects.count(), 0)

    def test_submission_anonymous_bert_large(self):
        submission = self.c.post('/api/submission/make_submission', data={'content': self.en, 'model': 'bert-large'})
        self.assertEqual(submission.status_code, 400)
        self.assertEqual(submission.json()['error'], ['Bez konta nie można korzystać z modelu LARGE.'])
        self.assertEqual(Submission.objects.count(), 0)

    def test_submission_anonymous_file_too_big(self):
        with open(os.path.join('model', 'data', 'unit_test', 'file_10.csv')) as f:
            submission = self.c.post(
                '/api/submission/make_submission',
                data={'model': 'bert-base', 'content': f}
            )
            self.assertEqual(submission.status_code, 400)
            self.assertEqual(len(submission.json()['error']), 1)
            self.assertEqual(Submission.objects.count(), 0)

    def test_submission_anonymous_wrong_file_extension(self):
        with open(os.path.join('model', 'data', 'unit_test', 'wrong_ext.txt')) as f:
            submission = self.c.post(
                '/api/submission/make_submission',
                data={'model': 'bert-base', 'content': f}
            )
            self.assertEqual(submission.status_code, 400)
            self.assertEqual(len(submission.json()['error']), 1)
            self.assertEqual(Submission.objects.count(), 0)

    def test_submission_anonymous_wrong_column_name(self):
        with open(os.path.join('model', 'data', 'unit_test', 'wrong_column.csv')) as f:
            submission = self.c.post(
                '/api/submission/make_submission',
                data={'model': 'bert-base', 'content': f}
            )
            self.assertEqual(submission.status_code, 400)
            self.assertEqual(len(submission.json()['error']), 1)
            self.assertEqual(Submission.objects.count(), 0)

    def test_submission_anonymous_wrong_model(self):
        submission = self.c.post(
            '/api/submission/make_submission',
            data={'model': 'bercik', 'content': self.en}
        )
        response_data = submission.json()
        self.assertEqual(submission.status_code, 400)
        self.assertEqual(response_data['error'], ['Niepoprawna nazwa modelu.'])
        self.assertEqual(Submission.objects.count(), 0)

    def test_submission_wrong_language(self):
        submission = self.c.post(
            '/api/submission/make_submission',
            data={'model': 'bert-base', 'content': 'Nie lubię tego robić.'}
        )
        response_data = submission.json()
        self.assertEqual(submission.status_code, 400)
        self.assertEqual(response_data['error'], ['Wykryty język nie jest obsługiwany. Podaj dane w języku angielskim.'])
        self.assertEqual(Submission.objects.count(), 0)

    def test_submission_anonymous_correct(self):
        submission = self.c.post('/api/submission/make_submission', data={'content': self.en, 'model': 'bert-base'})
        self.assertEqual(submission.status_code, 201)
        self.assertEqual(submission.json()['success'], 'Poprawnie przeprowadzono obliczenia.')


class TestUserSubmission(TestCase):
    def setUp(self):
        normal = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': make_password('Abecadło123!'),
            'usertype': 0,
            'username': 'normal_account',
            'is_verified': True
        }
        pro = {
            'name': 'Hubert Kłosowski',
            'email': 'a@a.pl',
            'password': make_password('Abecadło123!'),
            'usertype': 1,
            'username': 'pro_account',
            'is_verified': True
        }
        admin = {
            'name': 'Hubert Kłosowski',
            'email': 'a1@a1.pl',
            'password': make_password('Abecadło123!'),
            'usertype': 2,
            'submission_num': 0,
            'username': 'admin_account',
            'is_verified': True
        }

        self.normal = User.objects.create(**normal)
        self.pro = User.objects.create(**pro)
        self.admin = User.objects.create(**admin)

        self.c = Client()
        normal['password'] = 'Abecadło123!'
        self.token_normal = self.c.post('/api/user/login_user', data=normal).json()['access']
        pro['password'] = 'Abecadło123!'
        self.token_pro = self.c.post('/api/user/login_user', data=pro).json()['access']
        admin['password'] = 'Abecadło123!'
        self.token_admin = self.c.post('/api/user/login_user', data=admin).json()['access']

    def test_submission_user_not_exists(self):
        self.normal.delete()
        self.assertEqual(Submission.objects.count(), 0)
        response = self.c.post(
            '/api/submission/make_submission',
            data={'content': 'Check if I have depression.', 'model': 'bert-large'},
            headers={'Authorization': f'Bearer {self.token_normal}'}
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], ['Nie można potwierdzić uprawnień użytkownika do zasobu.'])
        self.assertEqual(Submission.objects.count(), 0)

    def test_submission_normal_too_big_file(self):
        with open(os.path.join('model', 'data', 'unit_test', 'file_20.csv'), encoding="utf8") as f:
            response = self.c.post(
                '/api/submission/make_submission',
                data={'content': f, 'model': 'bert-large'},
                headers={'Authorization': f'Bearer {self.token_normal}'}
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(len(response.json()['error']), 1)
            self.assertEqual(Submission.objects.count(), 0)

    def test_submission_pro_too_big_file(self):
        with open(os.path.join('model', 'data', 'unit_test', 'file_100.csv'), encoding="utf8") as f:
            response = self.c.post(
                '/api/submission/make_submission',
                data={'content': f, 'model': 'bert-large'},
                headers={'Authorization': f'Bearer {self.token_pro}'}
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(len(response.json()['error']), 1)
            self.assertEqual(Submission.objects.count(), 0)

    def test_submission_user_zero_trials(self):
        response = self.c.post(
            '/api/submission/make_submission',
            data={'content': 'Check if I have depression.', 'model': 'bert-base'},
            headers={'Authorization': f'Bearer {self.token_admin}'}
        )

        response_data = response.json()
        self.assertEqual(Submission.objects.count(), 0)
        self.assertIn('Użytkownik nie posiada wolnych prób.', response_data['error'])

    def test_submission_correct(self):
        response = self.c.post(
            '/api/submission/make_submission',
            data={'content': 'Check if I have depression.', 'model': 'bert-large'},
            headers={'Authorization': f'Bearer {self.token_normal}'}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Submission.objects.count(), 1)
        self.assertEqual(response.json()['success'], 'Poprawnie przeprowadzono obliczenia.')


class TestSubmissionReadUpdate(TestCase):
    def setUp(self):
        normal = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': make_password('Abecadło123!'),
            'usertype': 0,
            'username': 'normal_account',
            'is_verified': True
        }
        self.normal = User.objects.create(**normal)
        self.c = Client()
        normal['password'] = 'Abecadło123!'
        self.token_normal = self.c.post('/api/user/login_user', data=normal).json()['access']
        self.submission = self.c.post(
            '/api/submission/make_submission',
            data={'content': 'Check if I have depression.', 'model': 'bert-base'},
            headers={'Authorization': f'Bearer {self.token_normal}'}
        ).json()

    def test_submission_read_not_exists(self):
        sub_uuid = str(uuid.uuid4())
        submission = self.c.get(
            f'/api/submission/get_submission/{sub_uuid}',
            headers={'Authorization': f'Bearer {self.token_normal}'}
        )

        self.assertEqual(submission.status_code, 404)
        self.assertEqual(submission.json()['error'], ['Baza danych nie zawiera informacji o żądanej próbie.'])

    def test_submission_read_file_deleted(self):
        os.remove(os.path.join('media', 'submission_files', self.submission['submission']['content'].split('/')[-1]))
        self.assertEqual(Submission.objects.count(), 1)

        read = self.c.get(
            f'/api/submission/get_submission/{self.submission['submission']['id']}',
            headers={'Authorization': f'Bearer {self.token_normal}'}
        )
        self.assertEqual(read.status_code, 404)
        self.assertEqual(read.json()['error'], ['Plik z wskazanej próby nie istnieje.'])

    def test_submission_read_correct(self):
        read = self.c.get(
            f'/api/submission/get_submission/{self.submission['submission']['id']}',
            headers={'Authorization': f'Bearer {self.token_normal}'},
            content_type='application/json'
        )

        self.assertEqual(read.status_code, 200)
        self.assertEqual(read.json()['success'], 'Poprawnie odczytano dane.')

    def test_submission_change_name_not_exists(self):
        sub_uuid = str(uuid.uuid4())
        change_name = self.c.patch(
            f'/api/submission/change_name/{sub_uuid}',
            headers={'Authorization': f'Bearer {self.token_normal}'}
        )

        self.assertEqual(change_name.status_code, 404)
        self.assertEqual(change_name.json()['error'], ['Baza danych nie zawiera informacji o żądanej próbie.'])

    def test_submission_change_name_not_given_new_name(self):
        change_name = self.c.patch(
            f'/api/submission/change_name/{self.submission['submission']['id']}',
            data={'not_name': 'abecadlo'},
            headers={'Authorization': f'Bearer {self.token_normal}'},
            content_type='application/json'
        )

        after = change_name.json()
        self.assertEqual(change_name.status_code, 400)
        self.assertEqual(after['error'], ['Brak nowej nazwy do zmiany.'])

    def test_submission_change_name_correct(self):
        change_name = self.c.patch(
            f'/api/submission/change_name/{self.submission['submission']['id']}',
            data={'name': 'abecadlo'},
            headers={'Authorization': f'Bearer {self.token_normal}'},
            content_type='application/json'
        )

        response = change_name.json()
        self.assertEqual(change_name.status_code, 200)
        self.assertEqual(response['success'], 'Poprawnie ustawiono nazwę próby.')
        self.assertEqual(response['submission']['name'], 'abecadlo')
        self.assertEqual(self.submission['submission']['name'], None)