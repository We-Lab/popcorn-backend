from rest_framework import generics
from rest_framework import permissions

from movie.models import Comment, FamousLine
from movie.serializers.comment import CommentSerializer
from movie.serializers.famous_line import FamousLineSerializer


class MyComments(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(author=user)


class MyFamousLines(generics.ListAPIView):
    serializer_class = FamousLineSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return FamousLine.objects.filter(author=user)
