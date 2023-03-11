from rest_framework import permissions


class IsAuthorModeratorAdminSuperuserOrReadOnly(permissions.BasePermission):
    """Changes can be done by moderator/admin/superuser/object author."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminSuperuserOrReadOnly(permissions.BasePermission):
    """Changes can be done only by admin/superuser."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )
