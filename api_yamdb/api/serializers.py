import datetime

from django.core.exceptions import ValidationError
from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        lookup_field = "slug"
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        lookup_field = "slug"
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    """Serializer to add Titles."""

    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = "__all__"

    def validate_year(self, value):
        if value > datetime.datetime.now().year:
            raise ValidationError(
                "Неверный год выпуска. Измените дату выхода."
            )
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    """Serializer to read Titles."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"
        read_only_fields = ("id",)


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["view"].kwargs.get("titles_id")

    def __repr__(self):
        return f"{self.__class__.__name__}"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.HiddenField(
        default=CurrentTitleDefault(),
    )

    class Meta:
        fields = "__all__"
        model = Review

    def validate(self, data):
        if self.context["request"].method == "POST":
            author = self.context["request"].user
            title = self.context.get("view").kwargs.get("title_id")
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    "Не более одного комментария для произведения"
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
