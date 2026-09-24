from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class SchoolPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.role == "ADMIN"
        )