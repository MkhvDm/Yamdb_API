from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, ReviewViewSet, SignUpViewSet,
                    TokenObtainView, TitleViewSet, CategoriesViewSet,
                    GenresViewSet)

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
    TitleViewSet, basename='genres'
)


urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path(
        'v1/auth/token/', TokenObtainView.as_view(), name='token_obtain_pair'
    ),
]
