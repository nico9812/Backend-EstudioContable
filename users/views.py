from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .validations import UserModel, custom_validation, passwordpatch_validation
from django.db.models import Q
from django.utils import timezone
from django.conf import settings



User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(groups__name='cliente')
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes =[TokenAuthentication]
    serializer_class = UserSerializer

    def dispatch(self, request, *args, **kwargs):
        # Obtener el token de autenticación del encabezado de la solicitud
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        try:
            token = Token.objects.get(key=token)
        except Exception as e:
            return self.unauthorized_response()
        ahora = timezone.now()
        diferencia_segundos = (ahora - token.created).total_seconds()
        if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
            token.delete()
            return self.unauthorized_response()

        if token:
            user = token.user
            group = user.groups.all().first().id
            print(user.username, group, token)
            if group != 1:
                return self.unauthorized_response()
        return super().dispatch(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        id = kwargs['pk']
        user = UserModel.objects.get(pk=id)
        try:
            clean_data = passwordpatch_validation(request.data,id)
            serializer = UserSerializer(instance=user,data=clean_data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user.set_password(clean_data['password'])
                user.save()
                return Response(status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)




        
    
    def unauthorized_response(self):
        response = Response(status=status.HTTP_401_UNAUTHORIZED)
        response.accepted_renderer = self.get_renderers()[0]
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response

    

class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    ##
    def post(self, request):
        try:
            data = request.data
            serializer = UserLoginSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                user = User.objects.get(username=serializer.data['username'])
                grupo = user.groups.all().first()
                grupo = grupo.id if grupo else None

                if user:
                    token = Token.objects.get_or_create(user = user)
                    if token:
                        datos ={
                            'token':token[0].key,
                            'username':user.username,
                            'group':grupo,
                            'id':user.id,
                        }
                        return Response(datos, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_418_IM_A_TEAPOT)
        return Response(status=status.HTTP_418_IM_A_TEAPOT)
    
class UserDatosSession(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes =[TokenAuthentication]
    ##
    def post(self, request, user_id):
        try:
            user = User.objects.get(id= user_id)
            grupo = user.groups.all().first()
            grupo = grupo.id if grupo else None

            if user:
                token = Token.objects.get_or_create(user = user)

                if token.user.id == user_id:
                    datos ={
                        'token':token[0].key,
                        'username':user.username,
                        'group':grupo,
                        'id':user.id,
                    }
                    return Response(datos, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors': e.detail}, status=status.HTTP_418_IM_A_TEAPOT)
        return Response(status=status.HTTP_418_IM_A_TEAPOT)



class registerUser(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes =[TokenAuthentication]

    def post(self,request):
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
    

class UserSearchAPIView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes =[TokenAuthentication]

    def get(self, request,search,format=None):
        try:
            token = Token.objects.get(key=request.auth)
            ahora = timezone.now()
            diferencia_segundos = (ahora - token.created).total_seconds()
            if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
                token.delete()
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        ahora = timezone.now()
        diferencia_segundos = (ahora - token.created).total_seconds()
        if diferencia_segundos > getattr(settings, 'TOKEN_EXPIRATION'):
            token.delete()
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = token.user
        group = user.groups.all().first().id
        if group == 1:
            if search is not None and search != '':
                # Obtener el modelo de usuario
                User = get_user_model()


                users = User.objects.filter(
                    Q(first_name__icontains=search,) |  # Busca en atributo1
                    Q(last_name__icontains=search) |  # Busca en atributo2
                    Q(username__icontains=search) |  # Busca en atributo3, y así sucesivamente
                    Q(email__icontains=search),
                    groups__id=2
                ) 

                serializer = UserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"mensaje": "Por favor, proporcione una palabra clave para buscar."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje": "Sin permisos."}, status=status.HTTP_401_UNAUTHORIZED)
        
class Logout(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    authentication_classes =[TokenAuthentication]

    def get(self, request):
        # Borra el token del usuario al cerrar la sesión
        print(request.auth)
        if request.auth:
            request.auth.delete()
            return Response({'detail': 'Logout successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No token found.'}, status=status.HTTP_400_BAD_REQUEST)
        

    