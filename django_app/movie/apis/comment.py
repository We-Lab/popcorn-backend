from django.db.models import Count
from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from member.models import MyUser
from movie.models import Comment, Movie, CommentLike
from movie.permissions import IsOwnerOrReadOnly
from movie.serializers.comment import CommentSerializer, CommentLikeSerializer


class CommentAPIView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(movie=kwargs.get('movie_id')).order_by('-created_date')
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(comments, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    ######################################################################
    # refer to mixins.ListModelMixin and generics.GenericAPIView
    ######################################################################
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

        ######################################################################
        # refer to mixins.ListModelMixin and generics.GenericAPIView
        ######################################################################

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


class TopCommentView(APIView):
    # django Aggregation API 활용
    # 참조: https://docs.djangoproject.com/en/1.10/topics/db/aggregation/
    def get(self, request, *args, **kwargs):
        top_comment = Comment.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:3]
        serializer = CommentSerializer(top_comment, many=True)
        return Response(serializer.data)
