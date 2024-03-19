from rest_framework import viewsets, permissions, status
from .models import Vencimiento
from .serializer import VencimientoSerializer, VencimientoSerializerWithPropietarioName
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from users.authentication import ExpiringTokenAuthentication
from users.permissions import IsContador, IsCliente, IsOwner
from datetime import datetime, timedelta


class VencimientosUsuarioView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, usuario_id, mes, anio):
        token = Token.objects.get(key=request.auth)
        if token:
            user = token.user
            group = user.groups.all().first().id
            if user.id == usuario_id or group == 1:
                if 1 <= mes <= 12 and len(str(anio)) == 4:
                    vencimientos = Vencimiento.objects.filter(
                        propietario__id=usuario_id,
                        fecha__month=mes,
                        fecha__year=anio,
                    )

                    vencimientos_mensuales = Vencimiento.objects.filter(
                        propietario__id=usuario_id,
                        fecha__month__lt=mes,
                        fecha__year=anio,
                        mensualidad=True,
                    )
                    vencimientos = vencimientos.union(vencimientos_mensuales)

                    serializer = VencimientoSerializer(vencimientos, many=True)

                    # Modificar los vencimientos con mensualidad activa
                    nuevos_vencimientos = []
                    for vencimiento in serializer.data:
                        if vencimiento['mensualidad']:
                            fecha_actual = datetime.strptime(
                                vencimiento['fecha'], '%Y-%m-%d')
                            mes_actual = fecha_actual.month
                            if mes_actual != mes:
                                nueva_fecha = fecha_actual.replace(month=mes)
                                vencimiento['fecha'] = nueva_fecha.strftime(
                                    '%Y-%m-%d')

                    # Unir los vencimientos originales con los nuevos generados
                    vencimientos_data = serializer.data + nuevos_vencimientos

                else:
                    return Response({"error": "Mes o año proporcionados son inválidos"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(vencimientos_data)

    # def handle_exception(self, exc):
    #     # Imprimir el error
    #     print("Error en la vista del programa:", exc)

    #     # Devolver una respuesta de error al cliente
    #     return Response(
    #         {"detail": "Ocurrió un error en el servidor."},
    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #     )


class VencimientoContaViewSet(viewsets.ModelViewSet):
    queryset = Vencimiento.objects.filter()
    serializer_class = VencimientoSerializer
    authentication_classes = [ExpiringTokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, IsContador]

    def create(self, request, *args, **kwargs):
        # Obtenemos los datos del request
        data = request.data

        # Convertimos la fecha del formato string a objeto datetime
        fecha = datetime.strptime(data['fecha'], '%Y-%m-%d')

        # Obtener el día del mes
        dia = fecha.day

        # Si el día es mayor a 28, poner mensualidad en False
        if dia > 28:
            data['mensualidad'] = False

        # Llamamos al método create del padre (superclass)
        return super().create(request, *args, **kwargs)    
    
    def update(self, request, *args, **kwargs):
        # Obtenemos los datos del request
        # partial = kwargs.pop('partial', False)
        # instance = self.get_object()
        data = request.data

        # Convertimos la fecha del formato string a objeto datetime
        fecha = datetime.strptime(data['fecha'], '%Y-%m-%d')

        # Obtener el día del mes
        dia = fecha.day

        # Si el día es mayor a 28, poner mensualidad en False
        if dia > 28:
            data['mensualidad'] = False

        # Llamamos al método update del padre (superclass)
        return super().update(request, *args, **kwargs)


class VencimientosRecientes(APIView):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = datetime.now().date()
        seven_days_from_now = today + timedelta(days=7)

        ifContador = request.user.groups.filter(name="contador").exists()

        if ifContador:
            queryset = Vencimiento.objects.filter(
                fecha__range=[today, seven_days_from_now]).order_by('fecha')[:3]
        else:
            queryset = Vencimiento.objects.filter(propietario=request.user, fecha__range=[
                                                  today, seven_days_from_now]).order_by('fecha')[:3]

        serializer = VencimientoSerializerWithPropietarioName(
            queryset, many=True)
        return Response(serializer.data)