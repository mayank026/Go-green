from django.core.mail import send_mail

from django.conf import settings 


def send_forget_password_mail(email , token ):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/reset-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def send_mail_after_registration(email , token ):
    subject = 'Verify your account'
    message = f'Hi , click on the link to verify your account http://127.0.0.1:8000/verify-account/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def mail_to_admin(context):
    subject = 'Contact'
    name=context['name']
    emails=context['email']
    msg=context['message']
    message = f'Hi,{name} wants to contact you, kindly reach at {emails} and messages : {msg} '
    email_from = settings.EMAIL_HOST_USER
    email='bookhouse229@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
