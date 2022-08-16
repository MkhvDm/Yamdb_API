from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ProfileAPIView, ReviewViewSet, SelfProfileAPIView,
                    SignUpAPIView, TitleViewSet, UsersAPIView, TokenObtainView)

router_api_v1 = DefaultRouter()
router_api_v1.register(
    r'titles\/(?P<title_id>\d+)\/reviews',
    ReviewViewSet, basename='reviews'
)
router_api_v1.register(
    r'titles\/(?P<title_id>\d+)\/reviews\/(?P<review_id>\d+)\/comments',
    CommentViewSet, basename='comments'
)

router_api_v1.register(
    'titles',
    TitleViewSet, basename='titles'
)
router_api_v1.register(
    'categories',
    CategoriesViewSet, basename='categories'
)
router_api_v1.register(
    'genres',
    GenresViewSet, basename='genres'
)


urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path('v1/auth/signup/', SignUpAPIView.as_view(), name='signup'),
    path(
        'v1/auth/token/', TokenObtainView.as_view(), name='token_obtain'
    ),
    path('v1/users/', UsersAPIView.as_view(), name='users'),
    path('v1/users/me/', SelfProfileAPIView.as_view(), name='self_profile'),
    re_path(
        r'^v1/users/(?P<username>[\w.@+-]+)/$',
        ProfileAPIView.as_view(),
        name='profile'
    ),
]
