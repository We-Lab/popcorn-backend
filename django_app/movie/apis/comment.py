import random

from operator import attrgetter
from django.db.models import Count
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import MyUser
from movie.models import Comment, Movie, CommentLike, BoxOfficeMovie
from movie.permissions import IsOwnerOrReadOnly
from movie.serializers.comment import CommentSerializer, CommentLikeSerializer, MyCommentStarSerializer
from mysite.utils.profanities_filter import ProfanitiesFilter


class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CursorPagination

    def get_queryset(self):
        movie_pk = self.kwargs['pk']
        return Comment.objects.filter(movie=movie_pk)

    def perform_create(self, serializer):
        movie = Movie.objects.get(pk=self.kwargs['pk'])
        author = MyUser.objects.get(pk=self.request.user.pk)
        # 욕설 필터링 시작
        try:
            content = self.request.data['content']
            r = ProfanitiesFilter()
            clean_content = r.clean(content)
        except:
            clean_content = ''
        # 욕설 필터링 끝
        if Comment.objects.filter(movie=movie, author=author).exists():
            raise NotAcceptable('이미 코멘트를 작성했습니다')
        serializer.save(movie=movie, author=author, content=clean_content)
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
        # 욕 필터링 시작
        try:
            content = self.request.data['content']
            r = ProfanitiesFilter()
            clean_content = r.clean(content)
        except:
            clean_content = serializer.instance.content
        # 욕 필터링 끝
        old_star = instance.star
        new_star = float(self.request.data['star'])

        if old_star == new_star:
            serializer.save(content=clean_content)
        else:
            movie.star_sum -= old_star
            movie.star_sum += new_star
            # 평점 계산
            movie.star_average = ((movie.star_average * movie.comment_count) - old_star + new_star) / movie.comment_count
            movie.save()
            serializer.save(content=clean_content)

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
        try:
            comment = Comment.objects.get(pk=kwargs['pk'])
        except:
            raise NotAcceptable('댓글이 존재하지 않습니다.')
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
        comments = Comment.objects.filter(movie=self.kwargs['pk'])
        top_comment = comments.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:3]
        serializer = CommentSerializer(top_comment, many=True)
        return Response(serializer.data)


class NewCommentAPIView(APIView):
    """
    최신 댓글에서 6개 출력합니다.
    별점만 있는 댓글 제외합니다.
    """
    def get(self, request, *args, **kwargs):
        comment = Comment.objects.exclude(content__isnull=True).exclude(content__exact='').order_by('-created')[:6]
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)


class BestComment(APIView):
    """
    베스트 코멘트를 하나 출력합니다
    => 금주 박스오피스에 속한 코멘트 중, 코멘트 좋아요 상위 5개 중 1개 랜덤 추출

    """
    def get(self, request, *args, **kwargs):
        box_office = BoxOfficeMovie.objects.all().order_by('-created')[:10]
        comments = []
        for i in box_office:
            comment = Comment.objects.filter(movie__pk=i.movie.pk)
            for k in comment:
                comments.append(k)
        print('첫번째', comments)
        comments = sorted(comments, key=attrgetter('likes_count'), reverse=True)
        comments = comments[:5]
        print('두번째', comments)
        if len(comments) == 0:
            raise NotAcceptable('코멘트가 없습니다')
        else:
            best_comment = random.sample(comments, 1)
        serializer = CommentSerializer(best_comment, many=True)
        return Response(serializer.data)


class MyCommentStarView(generics.RetrieveAPIView):
    serializer_class = MyCommentStarSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        movie = self.kwargs['pk']
        return Comment.objects.get(author=user, movie=movie)


class StarHistogram(APIView):
    """
    별점 분포도입니다.

    """
    def get(self, request, *args, **kwargs):
        # ret = {}
        comment = Comment.objects.filter(movie=self.kwargs['pk'])
        comment_histogram = comment.values('star').annotate(count=Count('star')).order_by('-star')
        # for i in range(11):
        #     star = i * 0.5
        #     comment_star = comment.filter(star=star)
        #     ret[star] = len(comment_star)
        return Response(comment_histogram)
