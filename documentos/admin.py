from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import DocumentoPDF, Categoria

class DocumentoPDFAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'archivo_preview', 'propietario', 'categoria', 'is_active')
    search_fields = ('nombre', 'propietario__username')
    list_filter = ('categoria', 'is_active')
    readonly_fields = ('archivo_preview',)

    def archivo_preview(self, obj):
        # Muestra un enlace para previsualizar el archivo PDF
        if obj.archivo:
            return mark_safe(f'<a href="{obj.archivo.url}" target="_blank">Ver PDF</a>')
        return "No hay archivo adjunto."

    archivo_preview.allow_tags = True
    archivo_preview.short_description = 'Vista previa del archivo PDF'

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# Registra los modelos en el administrador
admin.site.register(DocumentoPDF, DocumentoPDFAdmin)
admin.site.register(Categoria, CategoriaAdmin)