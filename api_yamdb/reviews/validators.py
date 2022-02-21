from django.utils import timezone


def year_validator(value):
    if value > timezone.now().year:
        raise ValueError(
            'год некорректен',
            params={'value': value}
        )
