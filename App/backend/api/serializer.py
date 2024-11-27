from rest_framework import serializers
from .models import User, Submission
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': { 'write_only': True }
        }

    def validate(self, data):
        regex_name = re.compile(r'^[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+ [A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+$')
        if not regex_name.search(data['name']):
            raise serializers.ValidationError('Imie i nazwisko powinno składać się z dwóch wyrazów zaczynających się dużą literą.')

        if len(data['username']) < 8:
            raise serializers.ValidationError('Nazwa użytkownika powinna składać się z conajmniej 8 znaków')

        if 2 < data['usertype'] < 0:
            raise serializers.ValidationError('Nieznany typ użytkownika. Proszę wybrać między kontem STANDARD, PRO, ADMIN.')

        regex_email = re.compile(r'^\w+@\w+\.[a-zA-Z]{2,}$')
        if not regex_email.search(data['email']):
            raise serializers.ValidationError('Adres email musi być podany zgodnie z formatem: adres@mail.com')

        return data


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
