from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, ReviewViewSet, SignUpViewSet,
                    TokenObtainView)

router_api_v1 = DefaultRouter()
router_api_v1.register('auth/signup', SignUpViewSet, basename='signup')
router_api_v1.register(
    r'titles\/(?P<title_id>\d+)\/reviews',
    ReviewViewSet, basename='reviews'
)
router_api_v1.register(
    r'titles\/(?P<title_id>\d+)\/reviews\/(?P<review_id>\d+)\/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path(
        'v1/auth/token/', TokenObtainView.as_view(), name='token_obtain_pair'
    ),
]
