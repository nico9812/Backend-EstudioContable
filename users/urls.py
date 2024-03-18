from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserLogin, UserViewSet, registerUser, Logout, ValidateToken
# from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('userRegister/', registerUser.as_view(), name='registerUser'),
    path('userLogin/', UserLogin.as_view(), name='loginUser'),
    path('validate_token/', ValidateToken.as_view(), name='DatosSession'),
    path('logout/', Logout.as_view(), name='logout'),
]
