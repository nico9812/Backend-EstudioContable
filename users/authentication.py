from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key, request=None):
        models = self.get_model()

        try:
            token = models.objects.select_related("user").get(key=key)
        except models.DoesNotExist:
            raise AuthenticationFailed(
                {"error": "Token Invalido", "is_authenticated": False}
            )

        if not token.user.is_active:
            raise AuthenticationFailed(
                {"error": "Usuario Invalido", "is_authenticated": False}
            )

        ahora = timezone.now()
        diferencia_segundos = (ahora - token.created).total_seconds()

        if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
            token.delete()
            token.save()
            raise AuthenticationFailed(
                {"error": "Token Expirado", "is_authenticated": False}
            )
        return token.user, token
