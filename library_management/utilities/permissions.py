from rest_framework.permissions import BasePermission

from utilities.constants import ROLE_TYPES


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.role == ROLE_TYPES.student else False


class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.role == ROLE_TYPES.librarian else False


class IsExternalUser(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.role == ROLE_TYPES.external_user else False
