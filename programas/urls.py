from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramaViewSet, ProgramasUsuarioAPIView, ProSearchAPIView, ProgramasRecientes

router = DefaultRouter()
router.register(r'programas', ProgramaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('programa/<int:user_id>/',
         ProgramasUsuarioAPIView.as_view(), name='programas-usuario'),
    path('ProSearch/<str:search>/<int:id>/',
         ProSearchAPIView.as_view(), name='prosearch'),
    path('dashboard/programas_recientes',
         ProgramasRecientes.as_view(), name="programas_recientes")
]
