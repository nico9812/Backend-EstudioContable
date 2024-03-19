from django.urls import path, include
from .views import VencimientosUsuarioView, VencimientoContaViewSet, VencimientosRecientes
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vencimientos', VencimientoContaViewSet,
                basename='vencimientos_conta')

urlpatterns = [
    path('', include(router.urls)),
    path('vencimiento/<int:usuario_id>/<int:mes>/<int:anio>/',
         VencimientosUsuarioView.as_view(), name='vencimientos_cliente'),
    path('dashboard/vencimientos_recientes', VencimientosRecientes.as_view(),
         name='vencimientos_recientes')
]
