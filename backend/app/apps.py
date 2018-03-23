from django.apps import AppConfig


class LoginAttemptConfig(AppConfig):
    name = 'loginattempt'

    def ready(self):
        from .signals import log_user_logged_in_failed, log_user_logged_in_success
