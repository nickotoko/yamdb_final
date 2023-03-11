from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions, filters
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from users.serializers import (
    RegistrationSerializer,
    TokenSerializer,
    UserSerializer,
)
from .permissions import IsAdminOrSuperuser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    permission_classes = [
        IsAdminOrSuperuser,
    ]

    @action(
        detail=False,
        methods=["get", "put", "patch", "post"],
        url_path=r"v1/users/(?P<username>[\w.@+-]+)/$",
        url_name="username page",
        permission_classes=(IsAdminOrSuperuser,),
    )
    def get_self_page(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UserSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(data=request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "POST":
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(data=request.data)
            return JsonResponse(
                serializer.data, status=status.HTTP_204_NO_CONTENT
            )

    @action(
        detail=False,
        methods=["PATCH", "GET"],
        url_path="me",
        permission_classes=[
            permissions.IsAuthenticated,
        ],
    )
    def myself(self, request, pk=None):
        user = User.objects.get(username=request.user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(role=self.request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user, _ = User.objects.get_or_create(
            username=serializer.validated_data.get("username"),
            email=serializer.validated_data.get("email"),
        )

        confirmation_code = str(default_token_generator.make_token(user))
        message = ("Confirmation code to complete your registration",)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = (serializer.data["email"],)
        send_mail(
            message,
            confirmation_code,
            from_email,
            to_email,
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data.get("username")
    )
    token = Token.objects.get_or_create(user=user)
    if default_token_generator.check_token(
        user, str(serializer.validated_data.get("confirmation_code"))
    ):
        token = str(AccessToken.for_user(user))
        response = {"token": token}
        return Response(response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
