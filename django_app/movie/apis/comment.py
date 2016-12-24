""" 댓글 view module
1. 영화 댓글은 별점과 내용을 동시에 저장합니다.
2. 댓글 작성시 별점은 필수, 내용은 선택입니다.
3. 댓글 작성시 별점은 평균을 연산하여 movie table에 저장합니다. => ordering 가능
4. 좋아요 기능이 있습니다.
5. 댓글은 다양한 view로 출력합니다. (best, new, like top ....)
"""
import random

from operator import attrgetter
from django.db.models import Count
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import NotAcceptable, NotFound
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
        """
        1. 욕설 필터링을 포함
        2. 별점 작성시 평균 별점을 연산하여 movie 모델에 기입
        3. 유저 1인당 1개 댓글만 작성 가능
        """
        movie = Movie.objects.get(pk=self.kwargs['pk'])
        author = MyUser.objects.get(pk=self.request.user.pk)

        # 욕설 필터링
        try:
            content = self.request.data['content']
            r = ProfanitiesFilter()
            clean_content = r.clean(content)
        except:
            clean_content = ''

        if Comment.objects.filter(movie=movie, author=author).exists():
            raise NotAcceptable('이미 코멘트를 작성했습니다')
        serializer.save(movie=movie, author=author, content=clean_content)

        # 별점 평균 연산
        movie.comment_count += 1
        new_star = float(self.request.data['star'])
        movie.star_sum += new_star
        movie.star_average = (movie.star_average * (movie.comment_count - 1) + new_star) / movie.comment_count
        movie.save()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Comment.objects.all()

    def perform_update(self, serializer):
        """
        1. 욕설 필터링을 포함
        2. 별점 작성시 평균 별점을 연산하여 movie 모델에 기입
        """
        instance = serializer.instance
        movie_pk = instance.movie.pk
        movie = Movie.objects.get(pk=movie_pk)

        # 욕 필터링
        try:
            content = self.request.data['content']
            r = ProfanitiesFilter()
            clean_content = r.clean(content)
        except:
            clean_content = serializer.instance.content

        # 별점 평균 연산
        old_star = instance.star
        new_star = float(self.request.data['star'])
        if old_star == new_star:
            serializer.save(content=clean_content)
        else:
            movie.star_sum -= old_star
            movie.star_sum += new_star
            movie.star_average = ((movie.star_average * movie.comment_count) - old_star + new_star) / movie.comment_count
            movie.save()
            serializer.save(content=clean_content)

    def perform_destroy(self, instance):
        movie_pk = instance.movie.pk
        movie = Movie.objects.get(pk=movie_pk)

        # 평점 계산
        movie.star_sum -= instance.star
        movie.comment_count -= 1
        if movie.comment_count == 0:
            movie.star_average = 0
        else:
            movie.star_average = ((movie.star_average * (movie.comment_count + 1)) - instance.star) / movie.comment_count
        movie.save()

        instance.delete()


class CommentLikeView(generics.CreateAPIView):
    """
    1. comment 좋아요
    2. post 요청시 좋아요 생성 또는 삭제
    """
    serializer_class = CommentLikeSerializer
    queryset = CommentLike.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=kwargs['pk'])
        except:
            raise NotFound('댓글이 존재하지 않습니다.')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 중복 클릭 시 좋아요 삭제
        comment_like_exist = CommentLike.objects.filter(user=request.user, comment=comment)
        if comment_like_exist.exists():
            comment_like_exist.delete()
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)

        serializer.save(comment=comment, user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TopCommentView(APIView):
    """
    댓글 좋아요 개수 상위 3개 출력
    """
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(movie=self.kwargs['pk'])
        top_comment = comments.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:3]
        serializer = CommentSerializer(top_comment, many=True)
        return Response(serializer.data)


class NewCommentAPIView(APIView):
    """
    1. 최신 댓글에서 6개 출력
    2. 별점만 있는 댓글 제외
    """
    def get(self, request, *args, **kwargs):
        comment = Comment.objects.exclude(content__isnull=True).exclude(content__exact='').order_by('-created')[:6]
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)


class BestComment(APIView):
    """
    1. 베스트 코멘트를 하나 출력
    2. 금주 박스오피스에 속한 코멘트 중, 코멘트 좋아요 상위 5개 중 1개 랜덤 추출
    3. ios 전용
    """
    def get(self, request, *args, **kwargs):
        box_office = BoxOfficeMovie.objects.all().order_by('-created')[:10]

        # 박스오피스 안에 있는 댓을 리스트업
        comments = []
        for i in box_office:
            comment = Comment.objects.filter(movie__pk=i.movie.pk)
            for k in comment:
                comments.append(k)
        # print('첫번째', comments)

        # 5개 뽑아서 1개 랜덤 출력
        comments = sorted(comments, key=attrgetter('likes_count'), reverse=True)
        comments = comments[:5]
        # print('두번째', comments)
        if len(comments) == 0:
            raise NotAcceptable('코멘트가 없습니다')
        else:
            best_comment = random.sample(comments, 1)

        serializer = CommentSerializer(best_comment, many=True)
        return Response(serializer.data)


class MyCommentStarView(generics.RetrieveAPIView):
    """
    유저의 별점 출력
    """
    serializer_class = MyCommentStarSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        movie = self.kwargs['pk']
        return Comment.objects.get(author=user, movie=movie)


class StarHistogram(APIView):
    """
    별점 분포도
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
