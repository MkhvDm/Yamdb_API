from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import SignUpViewSet, TokenObtainView

router_api_v1 = DefaultRouter()
router_api_v1 .register('auth/signup', SignUpViewSet, basename='signup')

urlpatterns = [
    path('v1/', include(router_api_v1 .urls)),
    path(
        'v1/auth/token/', TokenObtainView.as_view(), name='token_obtain_pair'
    ),
    path(
        'v1/redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
