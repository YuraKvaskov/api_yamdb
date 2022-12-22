from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_HOST_USER


def send_confirmation_code_to_mail(email, confirmation_code):
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш новый код подтверждения для доступа: {confirmation_code}',
        from_email=EMAIL_HOST_USER,
        recipient_list=(email,),
        fail_silently=False,
    )