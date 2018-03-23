from .models import LoginAttempt
from django.contrib.auth import user_logged_in, user_login_failed
from django.dispatch import receiver
from backend.utils import HelperClass

@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    try:
        ip_login = HelperClass.get_client_ip(request)
        attempt, created = LoginAttempt.objects.get_or_create(ip=ip_login)
        attempt.success()
    except Exception as e:
        pass


@receiver(user_login_failed)
def log_user_logged_in_failed(sender, credentials, request, **kwargs):
    try:
        ip_login = HelperClass.get_client_ip(request)
        attempt, created = LoginAttempt.objects.get_or_create(ip=ip_login)
        attempt.fail()
    except Exception as e:
        pass