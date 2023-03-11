import datetime

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, mixins, serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import permission_classes, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from reviews.models import Category, Genre, Title, Review
from users.permissions import IsMyselfOrAdmin
from .filters import TitlesFilter
from .permissions import (
    IsAuthorModeratorAdminSuperuserOrReadOnly,
    IsAdminSuperuserOrReadOnly,
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
    CategorySerializer,
    GenreSerializer,
)


@api_view(["POST"])
@permission_classes((IsMyselfOrAdmin,))
def my_review(request):
    serializer = ReviewSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class MyBasicViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(MyBasicViewset):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination = PageNumberPagination
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(MyBasicViewset):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination = PageNumberPagination
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.annotate(rating=Avg("reviews__score"))
        .all()
        .order_by("name")
    )
    serializer_class = TitleCreateSerializer
    pagination = PageNumberPagination
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitlesFilter

    def validate_year(self, value):
        year = datetime.date.today().year
        if not value <= year:
            raise serializers.ValidationError(
                "Check the year, it cannot be in the future!"
            )
        return value

    def get_serializer_class(self):
        """Selects serializer for the request."""
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminSuperuserOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminSuperuserOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
