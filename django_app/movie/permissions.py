from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def __init__(self):
        self.message = '당신은 권한이 없습니다'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
