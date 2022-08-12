from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

from .views import CustomTokenObtainPairView, SignUpViewSet

router_v1 = DefaultRouter()
router_v1.register('auth/signup', SignUpViewSet, basename='signup')
#router_v1.register('auth/token', ConfirmationViewSet, basename='get_token')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'v1/redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
