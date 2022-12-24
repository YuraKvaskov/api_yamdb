from django.core.exceptions import ValidationError


def validate_score(value):
    if 11 <= value <= 0:
        raise ValidationError(
            'Недопустимое значение,'
            'оценка может быть от 1 до 10 включительно')
    return value
