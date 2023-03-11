from django.conf.urls import include
from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import UserViewSet, signup, get_token
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("titles", TitleViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="Reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", signup),
    path("v1/auth/token/", get_token),
]
