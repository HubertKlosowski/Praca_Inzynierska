from django.utils.translation import gettext_lazy as _
from rest_framework.test import APITestCase

from api.password_validation import LengthValidator, DigitValidator, CapitalLetterValidator, SpecialCharacterValidator
from api.serializer import UserSerializer, SubmissionSerializer

from api.models import User, Submission


class TestModels(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(**{
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 0,
            'username': 'normal_account',
            'is_verified': True
        })

        cls.submission = Submission.objects.create(**{
            'user_id': cls.user.id,
            'time_taken': 0,
            'model': 'bert-base',
            'content': 'submission_files/test.csv',
            'name': 'test'
        })

    def test_user_model_str(self):
        str_user = (
            f'User info\n name: {self.user.name}, email: {self.user.email}, '
            f'username: {self.user.username}, usertype: {self.user.usertype}, '
            f'created_at: {self.user.created_at}, submission_num: {self.user.submission_num}'
            f'last_submission: {self.user.last_submission}, is_verified: {self.user.is_verified}'
        )
        str_submission = (
            f'Submission info\n User:{self.user.username}, '
            f'Time (s): {self.submission.time_taken}, Model: {self.submission.model}'
        )

        self.assertNotEqual(str(self.user), '')
        self.assertEqual(str(self.user), str_user)
        self.assertNotEqual(str(self.submission), '')
        self.assertEqual(str(self.submission), str_submission)


class TestPasswordValidation(APITestCase):
    def test_password_length_validation(self):
        validator = LengthValidator()
        help_text = validator.get_help_text()

        self.assertEqual(
            help_text,
            _('Hasło musi mieć długość od 8 do 32 znaków.')
        )

    def test_password_digit_validation(self):
        validator = DigitValidator()
        help_text = validator.get_help_text()

        self.assertEqual(
            help_text,
            _('Hasło musi zawierać conajmniej 1 cyfr.')
        )

    def test_password_capital_letters(self):
        validator = CapitalLetterValidator()
        help_text = validator.get_help_text()

        self.assertEqual(
            help_text,
            _('Hasło musi zawierać conajmniej 1 dużych liter.')
        )

    def test_password_special_character_validation(self):
        validator = SpecialCharacterValidator()
        help_text = validator.get_help_text()

        self.assertEqual(
            help_text,
            _('Hasło musi zawierać conajmniej 1 znaków specjalnych.')
        )


class TestUserSerializer(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = {
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 0,
            'username': 'admin_account',
            'is_verified': True,
            'submission_num': 10
        }

    def test_user_serializer_wrong_name(self):
        self.user['name'] = 'hubercik'
        serializer = UserSerializer(data=self.user)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            str(serializer.errors['error'][0]),
            'Imie i nazwisko musi składać się z dwóch wyrazów zaczynających się dużą literą.'
        )

    def test_user_serializer_too_long_username(self):
        self.user['username'] = 'hubercik' * 7
        serializer = UserSerializer(data=self.user)

        self.assertEqual(len(self.user['username']), 56)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            str(serializer.errors['username'][0]),
            'Nazwa użytkownika nie może przekraczać 50 znaków.'
        )

    def test_user_serializer_too_long_email(self):
        self.user['email'] = f'hubercik@{'interia' * 10}.pl'
        serializer = UserSerializer(data=self.user)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            str(serializer.errors['email'][0]),
            'Adres email nie może przekraczać 50 znaków.'
        )

    def test_user_serializer_too_long_name(self):
        self.user['name'] = f'H{'uber' * 15} K{'łosowski' * 10}'
        serializer = UserSerializer(data=self.user)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            str(serializer.errors['name'][0]),
            'Imie i nazwisko nie może przekraczać 100 znaków.'
        )

    def test_user_serializer_wrong_usertype(self):
        self.user['usertype'] = 3
        serializer = UserSerializer(data=self.user)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            str(serializer.errors['error'][0]),
            'Nieznany typ użytkownika. Proszę wybrać między kontem STANDARD, PRO, ADMIN.'
        )

    def test_user_serializer_too_big_submission_num_submission_for_creating_normal(self):
        self.user['submission_num'] = 11
        serializer = UserSerializer(data=self.user)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            str(serializer.errors['error'][0]),
            'Dla zwykłego użytkownika liczba dziennych prób nie przekracza 10.'
        )

    def test_user_serializer_too_big_submission_num_submission_for_existing_normal(self):
        user_instance = User.objects.create(**self.user)
        serializer = UserSerializer(instance=user_instance, data={'submission_num': 11}, partial=True)
        user_instance.refresh_from_db()

        self.assertFalse(serializer.is_valid())
        self.assertTrue(user_instance.submission_num != 11)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(
            str(serializer.errors['error'][0]),
            'Dla zwykłego użytkownika liczba dziennych prób nie przekracza 10.'
        )

    def test_user_serializer_too_big_submission_num_submission_for_creating_pro(self):
        self.user['submission_num'] = 31
        self.user['usertype'] = 1
        serializer = UserSerializer(data=self.user)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            str(serializer.errors['error'][0]),
            'Dla użytkownika PRO liczba dziennych prób nie przekracza 30.'
        )

    def test_user_serializer_too_big_submission_num_for_existing_pro(self):
        self.user['usertype'] = 1
        user_instance = User.objects.create(**self.user)
        serializer = UserSerializer(instance=user_instance, data={'submission_num': 31}, partial=True)
        user_instance.refresh_from_db()

        self.assertFalse(serializer.is_valid())
        self.assertTrue(user_instance.submission_num != 31)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(
            str(serializer.errors['error'][0]),
            'Dla użytkownika PRO liczba dziennych prób nie przekracza 30.'
        )

    def test_user_serializer_too_big_submission_num_for_creating_admin(self):
        self.user['submission_num'] = 101
        self.user['usertype'] = 2
        serializer = UserSerializer(data=self.user)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            str(serializer.errors['error'][0]),
            'Dla administratora liczba dziennych prób nie przekracza 100.'
        )

    def test_user_serializer_too_big_submission_num_for_existing_admin(self):
        self.user['usertype'] = 2
        user_instance = User.objects.create(**self.user)
        serializer = UserSerializer(instance=user_instance, data={'submission_num': 101}, partial=True)
        user_instance.refresh_from_db()

        self.assertFalse(serializer.is_valid())
        self.assertTrue(user_instance.submission_num != 101)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(
            str(serializer.errors['error'][0]),
            'Dla administratora liczba dziennych prób nie przekracza 100.'
        )

    def test_user_serializer_correct(self):
        serializer = UserSerializer(data=self.user)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(User.objects.count(), 0)


class TestSubmissionSerializer(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(**{
            'name': 'Hubert Kłosowski',
            'email': 'hklosowski@interia.pl',
            'password': 'Abecadło123!',
            'usertype': 0,
            'username': 'normal_account',
            'is_verified': True
        })

        cls.submission = {
            'user_id': cls.user.id,
            'time_taken': 0,
            'model': 'bert-base',
            'content': 'submission_files/test.csv',
            'name': 'test'
        }

    def test_submission_too_long_name(self):
        self.submission['name'] = 'name' * 26
        serializer = SubmissionSerializer(data=self.submission)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(Submission.objects.count(), 0)
        self.assertEqual(
            str(serializer.errors['name'][0]),
            'Nazwa próby nie może przekraczać 100 znaków.'
        )