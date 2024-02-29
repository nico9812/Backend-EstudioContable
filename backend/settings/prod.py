from backend.settings.base import *

DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS_ARRAY', default='', cast=lambda v: [
    s.strip() for s in v.split(',')])

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS_ARRAY', default='', cast=lambda v: [
    s.strip() for s in v.split(',')])

# Configuración para enviar correos electrónicos
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.example.com'  # Configura el servidor SMTP que utilizarás para enviar correos electrónicos
# EMAIL_PORT = 587  # Puerto del servidor SMTP (generalmente 587 para TLS/STARTTLS)
# EMAIL_USE_TLS = True  # Configura si el servidor SMTP utiliza TLS/STARTTLS
# EMAIL_HOST_USER = 'your_email@example.com'  # Dirección de correo electrónico desde la cual enviar correos electrónicos
# EMAIL_HOST_PASSWORD = 'your_email_password'  # Contraseña de la dirección de correo electrónico
# DEFAULT_FROM_EMAIL = 'your_email@example.com'  # Dirección de correo electrónico predeterminada para enviar correos electrónicos

# # Opcional: Configurar el backend de correo electrónico en la consola para pruebas
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'