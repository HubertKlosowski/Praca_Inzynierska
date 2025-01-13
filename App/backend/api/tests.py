from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client

from api import custom_throttle
from api.models import User

custom_throttle.allow_request_for_test()


class TestLoginUser(TestCase):
    def setUp(self):
        user_verified = {
            'username': 'user_verified',
            'email': 'a@a.com',
            'password': make_password('passwd'),
            'name': 'test',
            'is_verified': True,
        }
        self.c = Client()
        self.user_verified = User.objects.create(**user_verified)

    def test_login_not_verified(self):
        user_not_verified = {
            'username': 'user_not_verified',
            'email': 'a1@a.com',
            'password': make_password('passwd'),
            'name': 'test1',
            'is_verified': False,
        }
        User.objects.create(**user_not_verified)
        response = self.c.post('/api/user/login_user', data=user_not_verified)
        self.assertEqual(response.status_code, 403)

    def test_login_not_exists(self):
        response = self.c.post('/api/user/login_user', data={'username': 'not', 'password': 'passwd'})
        self.assertEqual(response.status_code, 404)

    def test_login_bad_passsword(self):
        response = self.c.post('/api/user/login_user', data={'username': 'user_verified', 'password': 'passwd123'})
        self.assertEqual(response.status_code, 406)

    def test_login_correct(self):
        response = self.c.post('/api/user/login_user', data={'username': 'user_verified', 'password': 'passwd'})
        self.assertEqual(response.status_code, 200)


class TestCreateUser(TestCase):
    def setUp(self):
        self.c = Client()

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
        response = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(response.status_code, 406)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_empty(self):
        response = self.c.post('/api/user/create_user', data={})
        self.assertEqual(response.status_code, 406)

    def test_create_user_with_empty_fields(self):
        data = {
            'name': '',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account'
        }
        response = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(response.status_code, 406)

    def test_create_user_bad_password(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'abecadlo',
            'usertype': -1,
            'username': 'admin_account'
        }
        response = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.json()['error']), 3)
        data['password'] = 'abecadlo123'
        response = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.json()['error']), 2)
        data['password'] = 'abecadlo123!'
        response = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.json()['error']), 1)

    def test_create_user_wrong_usertype(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': -1,
            'username': 'admin_account'
        }
        response = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_wrong_email(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'ainteria.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account'
        }
        response = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_correct(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account'
        }
        response = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(response.status_code, 201)


class TestUpdateUser(TestCase):
    def setUp(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account'
        }
        self.user = User.objects.create(**data)
        self.c = Client()


class TestDeleteUser(TestCase):
    def setUp(self):
        self.data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account',
            'is_verified': True
        }
        self.c = Client()
        self.c.post('/api/user/create_user', data=self.data)

    def test_delete_user(self):
        login = self.c.post('/api/user/login_user', data=self.data)
        token = login.json()['access']
        self.assertEqual(User.objects.count(), 1)
        delete = self.c.delete('/api/user/delete_user', headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(delete.status_code, 200)
        delete_again = self.c.delete('/api/user/delete_user', headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(delete_again.status_code, 404)

    def test_delete_user_not_authorized(self):
        response = self.c.delete('/api/user/delete_user', data=self.data)
        self.assertEqual(response.status_code, 403)

