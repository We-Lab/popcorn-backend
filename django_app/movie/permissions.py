from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    작성자 권한 permission
    """
    def __init__(self):
        self.message = '당신은 권한이 없습니다'

    def has_object_permission(self, request, view, obj):
        """
        get 요청 이외 요청은 작성자만 true 출력
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
