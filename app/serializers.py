from django.contrib.auth import authenticate, user_logged_in, get_user_model

from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from backend.utils import HelperClass
from .models import *


class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            request = self.context['request']
            user = authenticate(request=request, **credentials)

            ip_login = HelperClass.get_client_ip(request)
            attempt, created = LoginAttempt.objects.get_or_create(ip=ip_login)

            if attempt.can_login():
                if user:
                    if not user.is_active:
                        msg = 'Uporabnik ni aktiven.'
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)
                    user_logged_in.send(sender=user.__class__, request=request, user=user)
                    attempt.success()

                    return {
                        'user': user,
                        'token': jwt_encode_handler(payload)
                    }
                else:
                    attempt.fail()
                    msg = 'Napačen vnos podatkov.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Vaš IP naslov je trenutno blokiran (preveč neveljavnih poskusov).'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'roles')


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }