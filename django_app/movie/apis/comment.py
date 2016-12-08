from django.db.models import Count
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import MyUser
from movie.models import Comment, Movie, CommentLike
from movie.permissions import IsOwnerOrReadOnly
from movie.serializers.comment import CommentSerializer, CommentLikeSerializer


class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CursorPagination

    def get_queryset(self):
        movie_pk = self.kwargs['pk']
        return Comment.objects.filter(movie_pk=movie_pk)

    def perform_create(self, serializer):
        movie = Movie.objects.get(pk=self.kwargs['pk'])
        author = MyUser.objects.get(pk=self.request.user.pk)
        serializer.save(movie=movie, author=author)
        movie.comment_count += 1
        new_star = float(self.request.data['star'])
        movie.star_sum += new_star
        # 평점 계산
        movie.star_average = (movie.star_average * (movie.comment_count - 1) + new_star) / movie.comment_count
        movie.save()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Comment.objects.all()

    def perform_update(self, serializer):
        instance = serializer.instance
        movie_pk = instance.movie.pk
        movie = Movie.objects.get(pk=movie_pk)
        old_star = instance.star
        new_star = float(self.request.data['star'])
        if old_star == new_star:
            serializer.save()
        else:
            movie.star_sum -= old_star
            movie.star_sum += new_star
            # 평점 계산
            movie.star_average = ((movie.star_average * movie.comment_count) - old_star + new_star) / movie.comment_count
            movie.save()
            serializer.save()

    def perform_destroy(self, instance):
        movie_pk = instance.movie.pk
        movie = Movie.objects.get(pk=movie_pk)
        movie.star_sum -= instance.star
        movie.comment_count -= 1
        # 평점 계산
        movie.star_average = ((movie.star_average * (movie.comment_count + 1)) - instance.star) / movie.comment_count
        movie.save()
        instance.delete()


class CommentLikeView(generics.CreateAPIView):
    serializer_class = CommentLikeSerializer
    queryset = CommentLike.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    # post 요청시 좋아요 생성 또는 삭제
    def create(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs['pk'])
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


class NewCommentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        comment = Comment.objects.all().order_by('-created')[:10]
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)
