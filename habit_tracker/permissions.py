from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "You are not an owner of this entity"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
