from django.contrib import admin

from .models import Programa

class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'resolucion', 'localidad', 'fecha_inicio', 'fecha_final', 'dias', 'profesional', 'estado', 'usuario')
    search_fields = ('nombre', 'profesional', 'usuario__nombre_usuario')  # Permite buscar por nombre, profesional y nombre de usuario del usuario asociado

admin.site.register(Programa, ProgramaAdmin)