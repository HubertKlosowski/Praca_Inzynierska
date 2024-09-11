from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class MinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _(f'BŁĄD!! Zbyt krótkie hasło (conajmniej {self.min_length} znaków).'),
            )

    def get_help_text(self):
        return _(
            f'Hasło musi mieć conajmniej {self.min_length} znaków.'
        )

class DigitValidator:
    def __init__(self, min_num=1):
        self.min_num = min_num

    def validate(self, password, user=None):
        regex = f'[0-9]{{{self.min_num}}}'
        if not re.search(regex, password):
            raise ValidationError(
                _(f'BŁĄD!! Hasło nie zawiera cyfr.')
            )

    def get_help_text(self):
        return _(
            f'Hasło musi zawierać conajmniej {self.min_num} cyfr.'
        )

class CapitalLetterValidator:
    def __init__(self, min_num=1):
        self.min_num = min_num

    def validate(self, password, user=None):
        regex = f'[A-Z]{{{self.min_num}}}'
        if not re.search(regex, password):
            raise ValidationError(
                _(f'BŁĄD!! Hasło nie zawiera dużych liter.')
            )

    def get_help_text(self):
        return _(
            f'Hasło musi zawierać conajmniej {self.min_num} dużych liter.'
        )

class SpecialCharacterValidator:
    def __init__(self, min_num=1):
        self.min_num = min_num

    def validate(self, password, user=None):
        regex = f'[~!@#$%^&*()_+:;?]{{{self.min_num}}}'
        if not re.search(regex, password):
            raise ValidationError(
                _(f'BŁĄD!! Hasło nie zawiera specjalnych znaków.')
            )

    def get_help_text(self):
        return _(
            f'Hasło musi zawierać conajmniej {self.min_num} znaków specjalnych.'
        )
