from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)


class HolidayPermission(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return True

        return request.user.role == "ADMIN"