import re

from rest_framework import serializers

from .models import User, Submission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True,
                'error_messages': {
                    'required': 'Hasło jest wymagane do utworzenia konta.'
                }
            },
            'name': {
                'error_messages': {
                    'required': 'Imię i nazwisko jest wymagane do utworzenia konta.'
                }
            },
            'username': {
                'error_messages': {
                    'required': 'Nazwa użytkownika jest wymagana do utworzenia konta.'
                }
            },
            'email': {
                'error_messages': {
                    'required': 'Adres email jest wymagany do utworzenia konta.'
                }
            },
            'usertype': {
                'error_messages': {
                    'required': 'Pole typ konta jest wymagane do utworzenia konta.'
                }
            },
            'last_submission': {
                'write_only': True,
            },
            'is_verified': {
                'write_only': True,
            },
            'created_at': {
                'write_only': True,
            },
            'last_login': {
                'write_only': True,
            }
        }

    def validate(self, data):
        if self.instance:
            if 'submission_num' in data:
                if data['submission_num'] > 10 and self.instance['usertype'] == 0:
                    raise serializers.ValidationError({
                        'error': 'Dla zwykłego użytkownika liczba dziennych prób nie przekracza 10.'
                    })
                elif data['submission_num'] > 30 and self.instance['usertype'] == 1:
                    raise serializers.ValidationError({
                        'error': 'Dla użytkownika PRO liczba dziennych prób nie przekracza 30.'
                    })
                elif data['submission_num'] > 40 and self.instance['usertype'] == 2:
                    raise serializers.ValidationError({
                        'error': 'Dla administratora liczba dziennych prób nie przekracza 100.'
                    })
        else:
            regex_name = re.compile(r'^[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+ [A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+$')
            if not regex_name.search(data['name']):
                raise serializers.ValidationError({
                    'error': 'Imie i nazwisko powinno składać się z dwóch wyrazów zaczynających się dużą literą.'
                })
            if len(data['username']) < 8:
                raise serializers.ValidationError({
                    'error': 'Nazwa użytkownika powinna składać się z conajmniej 8 znaków.'
                })
            if 2 < data['usertype'] < 0:
                raise serializers.ValidationError({
                    'error': 'Nieznany typ użytkownika. Proszę wybrać między kontem STANDARD, PRO, ADMIN.'
                })
            regex_email = re.compile(r'^\w+@\w+\.[a-zA-Z]{2,}$')
            if not regex_email.search(data['email']):
                raise serializers.ValidationError({
                    'error': 'Adres email musi być podany zgodnie z formatem: adres@mail.com.'
                })

        return data


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
