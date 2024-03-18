from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, DocumentoPDFViewSet, ProtectedMediaView, DocumentoPDFAPIView, DocumentosFiltrarCatView, DocumentosRecientes

router = DefaultRouter()
router.register(r'documentos', DocumentoPDFViewSet, basename='Documentos')
router.register(r'categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('', include(router.urls)),
    path('media/<int:id>/', ProtectedMediaView.as_view(),
         name='ProtectedMediaView'),
    path('documentoscli/<int:id>/', DocumentoPDFAPIView.as_view(),
         name='DocumentoPDFAPIView'),
    path('documentosFiltrar/<str:categoria>/<int:id>/',
         DocumentosFiltrarCatView.as_view(), name='Documentofiltrar'),
    path('dashboard/documentos_recientes', DocumentosRecientes.as_view(),
         name='documentos_recientes'),
]
