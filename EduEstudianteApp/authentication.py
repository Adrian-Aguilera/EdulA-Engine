from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from .models import PerfilEstudiante

class JWTAuthenticationEstudiante(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            if not user_id:
                raise AuthenticationFailed(_('User ID not found in token'))
            return PerfilEstudiante.objects.get(id=user_id)
        except PerfilEstudiante.DoesNotExist:
            raise AuthenticationFailed(_('User not found'))
        except KeyError:
            raise AuthenticationFailed(_('Invalid token'))
        except Exception as e:
            raise AuthenticationFailed(str(e))