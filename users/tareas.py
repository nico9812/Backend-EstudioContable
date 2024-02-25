# from django.core.mail import send_mail
from vencimientos.models import Vencimiento
from datetime import datetime,timedelta
import calendar

def enviar_correos():
    fecha_actual = datetime.now()
    ultimo_dia_mes_actual = calendar.monthrange(fecha_actual.year, fecha_actual.month)[1]
    fecha_limite = fecha_actual.replace(day=ultimo_dia_mes_actual) + timedelta(days=fecha_actual.day)
    alarmas = Vencimiento.objects.filter(alarma=True,fecha=fecha_limite)
    # # Lógica para enviar correos electrónicos
    # # Ejemplo de envío de correo
    # send_mail(
    #     'Asunto del correo',
    #     'Cuerpo del correo.',
    #     'remitente@example.com',
    #     ['destinatario@example.com'],
    #     fail_silently=False,
    # )

enviar_correos()