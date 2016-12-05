from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import MyUser
from movie.models import Comment, Movie, CommentLike
from movie.permissions import IsOwnerOrReadOnly
from movie.serializers.comment import CommentSerializer, CommentLikeSerializer


class CommentAPIView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(movie=kwargs.get('movie_id')).order_by('-created_date')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        movie = Movie.objects.get(id=kwargs.get('movie_id'))
        author = MyUser.objects.get(pk=request.user.pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):

    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, comment_id):
        try:
            obj = Comment.objects.get(id=comment_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        comment = self.get_object(comment_id=kwargs.get('comment_id'))
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        comment = self.get_object(comment_id=kwargs.get('comment_id'))
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object(comment_id=kwargs.get('comment_id'))
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentLikeView(generics.CreateAPIView):
    serializer_class = CommentLikeSerializer
    queryset = CommentLike.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    # post 요청시 좋아요 생성 또는 삭제
    def create(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs['comment_id'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment_like_exist = CommentLike.objects.filter(user=request.user, comment=comment)
        if comment_like_exist.exists():
            comment_like_exist.delete()
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)
        serializer.save(comment=comment, user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
