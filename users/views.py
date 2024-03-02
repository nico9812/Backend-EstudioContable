from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from users.authentication import ExpiringTokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .validations import UserModel, custom_validation, passwordpatch_validation
from .permissions import IsContador
from django.utils import timezone

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(groups__name='cliente')
    permission_classes = [permissions.IsAuthenticated, IsContador, ]
    authentication_classes = [ExpiringTokenAuthentication]
    serializer_class = UserSerializer

    def partial_update(self, request, *args, **kwargs):
        id = kwargs['pk']
        user = UserModel.objects.get(pk=id)
        try:
            clean_data = passwordpatch_validation(request.data, id)
            serializer = UserSerializer(
                instance=user, data=clean_data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user.set_password(clean_data['password'])
                user.save()
                return Response(status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def post(self, request):
        try:
            data = request.data
            serializer = UserLoginSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                user = User.objects.get(username=serializer.data['username'])
                grupo = user.groups.all().first()
                grupo = grupo.id if grupo else None

                if user:
                    try:
                        token = Token.objects.get(user=user)
                        token.created = timezone.now()  # Actualiza la fecha de creación del token
                        token.save()
                    except Token.DoesNotExist:
                        # Si no existe un token para el usuario, crea uno nuevo
                        token = Token.objects.create(user=user)

                    if token:
                        datos = {
                            'token': token.key,
                            'username': user.username,
                            'group': grupo,
                            'id': user.id,
                        }
                        return Response(datos, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDatosSession(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            grupo = user.groups.all().first()
            grupo = grupo.id if grupo else None

            if user:
                token = Token.objects.get_or_create(user=user)

                if token.user.id == user_id:
                    datos = {
                        'token': token[0].key,
                        'username': user.username,
                        'group': grupo,
                        'id': user.id,
                    }
                    return Response(datos, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class registerUser(APIView):
    permission_classes = [permissions.IsAuthenticated, IsContador]
    authentication_classes = [ExpiringTokenAuthentication]

    def post(self, request):
        try:
            clean_data = custom_validation(request.data)
            serializer = UserRegisterSerializer(data=clean_data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.create(clean_data)
                if user:
                    return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    def get(self, request):
        if request.auth:
            request.auth.delete()
            return Response({'detail': 'Logout successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No token found.'}, status=status.HTTP_400_BAD_REQUEST)
