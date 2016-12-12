from rest_framework import generics
from rest_framework import permissions

from member.models import MyUser
from member.serializers import MyInfoSerializer
from movie.models import Comment, FamousLine, MovieLike
from movie.serializers.comment import CommentSerializer
from movie.serializers.famous_line import FamousLineSerializer
from movie.serializers.movie import MovieMyLikeSerializer


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


class MyInfo(generics.RetrieveAPIView):
    serializer_class = MyInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        pk = self.request.user.pk
        return MyUser.objects.get(pk=pk)


class MyLikeMovie(generics.ListAPIView):
    """
    유저가 좋아요한 영화 리스트를 출력합니다.

    """
    serializer_class = MovieMyLikeSerializer
    permissions = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return MovieLike.objects.filter(user=user).order_by('-created')

