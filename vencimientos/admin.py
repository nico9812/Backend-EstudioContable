from django.contrib import admin
from .models import Vencimiento

class VencimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'alarma', 'propietario', 'is_active')
    search_fields = ('nombre', 'propietario__username')
    list_filter = ('alarma', 'is_active')
    date_hierarchy = 'fecha'

admin.site.register(Vencimiento, VencimientoAdmin)
