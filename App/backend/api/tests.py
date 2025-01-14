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

    def test_login_user_not_verified(self):
        user_not_verified = {
            'username': 'user_not_verified',
            'email': 'a1@a.com',
            'password': make_password('passwd'),
            'name': 'test1',
            'is_verified': False,
        }
        User.objects.create(**user_not_verified)
        login_not_verified = self.c.post('/api/user/login_user', data=user_not_verified)
        self.assertEqual(login_not_verified.status_code, 403)

    def test_login_user_not_exists(self):
        login_not_exists = self.c.post('/api/user/login_user', data={'username': 'not', 'password': 'passwd'})
        self.assertEqual(login_not_exists.status_code, 404)

    def test_login_user_bad_passsword(self):
        login_bad_passsword = self.c.post('/api/user/login_user', data={'username': 'user_verified', 'password': 'passwd123'})
        self.assertEqual(login_bad_passsword.status_code, 406)

    def test_login_user_correct(self):
        login_correct = self.c.post('/api/user/login_user', data={'username': 'user_verified', 'password': 'passwd'})
        self.assertEqual(login_correct.status_code, 200)


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
        create_already_exists = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(create_already_exists.status_code, 406)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_empty(self):
        test_create_user_empty = self.c.post('/api/user/create_user', data={})
        self.assertEqual(test_create_user_empty.status_code, 406)

    def test_create_user_with_empty_fields(self):
        data = {
            'name': '',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account'
        }
        create_with_empty_fields = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(create_with_empty_fields.status_code, 406)

    def test_create_user_too_short_password(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'New123!',
            'usertype': -1,
            'username': 'admin_account'
        }
        create_too_short_password = self.c.post('/api/user/create_user', data=data)
        response_data = create_too_short_password.json()
        self.assertEqual(create_too_short_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Zbyt krótkie hasło (min. 8 znaków).', response_data['error'])

    def test_create_user_too_long_password(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'New123!New123!New123!New123!New123!New123!New123!',
            'usertype': -1,
            'username': 'admin_account'
        }
        create_too_long_password = self.c.post('/api/user/create_user', data=data)
        response_data = create_too_long_password.json()
        self.assertEqual(create_too_long_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Zbyt długie hasła (max. 32 znaków).', response_data['error'])

    def test_create_user_no_digits_in_password(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'New!New!New!',
            'usertype': -1,
            'username': 'admin_account'
        }
        create_no_digits_in_password = self.c.post('/api/user/create_user', data=data)
        response_data = create_no_digits_in_password.json()
        self.assertEqual(create_no_digits_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera cyfr.', response_data['error'])

    def test_create_user_no_capital_letters_in_password(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'new123!new123!new123!',
            'usertype': -1,
            'username': 'admin_account'
        }
        create_no_capital_letters_in_password = self.c.post('/api/user/create_user', data=data)
        response_data = create_no_capital_letters_in_password.json()
        self.assertEqual(create_no_capital_letters_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera dużych liter.', response_data['error'])

    def test_create_user_no_special_characters_in_password(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'New123New123New123',
            'usertype': -1,
            'username': 'admin_account'
        }
        create_no_special_characters_in_password = self.c.post('/api/user/create_user', data=data)
        response_data = create_no_special_characters_in_password.json()
        self.assertEqual(create_no_special_characters_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera specjalnych znaków.', response_data['error'])

    def test_create_user_wrong_usertype(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': -1,
            'username': 'admin_account'
        }
        create_wrong_usertype = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(create_wrong_usertype.status_code, 400)

    def test_create_user_wrong_email(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'ainteria.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account'
        }
        create_wrong_email = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(create_wrong_email.status_code, 400)

    def test_create_user_correct(self):
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account'
        }
        create_correct = self.c.post('/api/user/create_user', data=data)
        self.assertEqual(create_correct.status_code, 201)


class TestUpdateUser(TestCase):
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

    def test_update_user_only_wrong_field(self):
        changed_data = {'usertype': 0}
        update_only_wrong_field = self.c.patch('/api/user/update_user',
                              data=changed_data,
                              headers={'Authorization': 'Bearer ' + self.token},
                              content_type='application/json')
        response_data = update_only_wrong_field.json()
        self.assertEqual(update_only_wrong_field.status_code, 406)
        self.assertEqual(response_data['error'], ['Można tylko zmienić tylko nazwę użytkownika, email, imię i hasło.'])

    def test_update_user_at_least_one_field(self):
        changed_data = {'username': '', 'email': '', 'password': 'newPassowrd123!@#'}
        update_at_least_one_field = self.c.patch('/api/user/update_user',
                              data=changed_data,
                              headers={'Authorization': 'Bearer ' + self.token},
                              content_type='application/json')
        response_data = update_at_least_one_field.json()
        self.assertEqual(update_at_least_one_field.status_code, 406)
        self.assertEqual(response_data['error'], ['Żadne pole nie może być puste.'])

    def test_update_user_not_exists(self):
        self.c.delete('/api/user/delete_user', headers={'Authorization': 'Bearer ' + self.token})
        changed_data = {'username': 'admin_account'}
        update_not_exists = self.c.patch('/api/user/update_user',
                              data=changed_data,
                              headers={'Authorization': 'Bearer ' + self.token},
                              content_type='application/json')
        response_data = update_not_exists.json()
        self.assertEqual(update_not_exists.status_code, 404)
        self.assertEqual(response_data['error'], ['Użytkownik nie istnieje.'])

    def test_update_user_forbidden(self):
        changed_data = {'username': 'admin_account_2'}
        update_forbidden = self.c.patch('/api/user/update_user', data=changed_data)
        self.assertEqual(update_forbidden.status_code, 403)

    def test_update_user_too_short_password(self):
        changed_data = {'password': 'New123!'}
        update_too_short_password = self.c.patch('/api/user/update_user',
                                                 data=changed_data,
                                                 headers={'Authorization': 'Bearer ' + self.token},
                                                 content_type='application/json')
        response_data = update_too_short_password.json()
        self.assertEqual(update_too_short_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Zbyt krótkie hasło (min. 8 znaków).', response_data['error'])

    def test_update_user_too_long_password(self):
        changed_data = {'password': 'New123!New123!New123!New123!New123!New123!New123!'}
        update_too_long_password = self.c.patch('/api/user/update_user',
                              data=changed_data,
                              headers={'Authorization': 'Bearer ' + self.token},
                              content_type='application/json')
        response_data = update_too_long_password.json()
        self.assertEqual(update_too_long_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Zbyt długie hasła (max. 32 znaków).', response_data['error'])

    def test_update_user_no_digits_in_password(self):
        changed_data = {'password': 'New!New!New!'}
        update_no_digits_in_password = self.c.patch('/api/user/update_user',
                                                    data=changed_data,
                                                    headers={'Authorization': 'Bearer ' + self.token},
                                                    content_type='application/json')
        response_data = update_no_digits_in_password.json()
        self.assertEqual(update_no_digits_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera cyfr.', response_data['error'])

    def test_update_user_no_capital_letters_in_password(self):
        changed_data = {'password': 'new123!new123!new123!'}
        update_no_capital_letters_in_password = self.c.patch('/api/user/update_user',
                                                             data=changed_data,
                                                             headers={'Authorization': 'Bearer ' + self.token},
                                                             content_type='application/json')
        response_data = update_no_capital_letters_in_password.json()
        self.assertEqual(update_no_capital_letters_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera dużych liter.', response_data['error'])

    def test_update_user_no_special_characters_in_password(self):
        changed_data = {'password': 'New123New123New123'}
        update_no_special_characters_in_password = self.c.patch('/api/user/update_user',
                                                                data=changed_data,
                                                                headers={'Authorization': 'Bearer ' + self.token},
                                                                content_type='application/json')
        response_data = update_no_special_characters_in_password.json()
        self.assertEqual(update_no_special_characters_in_password.status_code, 400)
        self.assertEqual(len(response_data['error']), 1)
        self.assertIn('Hasło nie zawiera specjalnych znaków.', response_data['error'])

    def test_update_user_correct(self):
        changed_data = {'username': 'admin_account_2'}
        update_correct = self.c.patch('/api/user/update_user',
                                      data=changed_data,
                                      headers={'Authorization': 'Bearer ' + self.token},
                                      content_type='application/json')
        self.assertEqual(update_correct.status_code, 200)


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
        login = self.c.post('/api/user/login_user', data=self.data)
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
        self.c = Client()
        data = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 2,
            'username': 'admin_account',
            'is_verified': True
        }
        self.c.post('/api/user/create_user', data=data)
        login = self.c.post('/api/user/login_user', data=data)
        self.token = login.json()['access']

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
