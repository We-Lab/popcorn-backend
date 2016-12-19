from django.db.models import Count
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import MyUser
from movie.models import FamousLine, Movie, Actor, FamousLike
from movie.permissions import IsOwnerOrReadOnly
from movie.serializers.famous_line import FamousLineSerializer, FamousLikeSerializer
from mysite.utils.profanities_filter import ProfanitiesFilter


class FamousLiseView(generics.ListCreateAPIView):
    serializer_class = FamousLineSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CursorPagination

    def get_queryset(self):
        movie_pk = self.kwargs['pk']
        # print(movie_pk)
        return FamousLine.objects.filter(movie=movie_pk)

    def perform_create(self, serializer):
        # print(self)
        movie_pk = self.kwargs['pk']
        movie = Movie.objects.get(pk=movie_pk)
        author = MyUser.objects.get(pk=self.request.user.id)
        a1 = Actor.objects.filter(movie=movie_pk)
        a2 = Actor.objects.get(pk=self.request.data['actor'])
        if a2 not in [i for i in a1]:
            raise NotAcceptable('해당 배우를 찾을 수 없습니다.')
        # 욕설 필터링 시작
        content = self.request.data['content']
        r = ProfanitiesFilter()
        clean_content = r.clean(content)
        # 욕설 필터링 끝
        serializer.save(movie=movie, actor=a2, author=author, content=clean_content)


class FamousLineDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FamousLineSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = FamousLine.objects.all()

    # get object 기본이 pk라 url 키워드 다 movie_pk -> pk로 변경함
    def perform_update(self, serializer):
        famous_pk = self.kwargs['pk']
        famous_line = FamousLine.objects.get(pk=famous_pk)
        movie_pk = famous_line.movie.pk
        actors = Actor.objects.filter(movie=movie_pk)
        actor = Actor.objects.get(pk=self.request.data['actor'])
        # 욕 필터링 시작
        try:
            content = self.request.data['content']
            r = ProfanitiesFilter()
            clean_content = r.clean(content)
        except:
            clean_content = serializer.instance.content
        # 욕 필터링 끝
        if actor not in [i for i in actors]:
            raise NotAcceptable('해당 배우를 찾을 수 없습니다.')
        serializer.save(content=clean_content)


class FamousLikeView(generics.CreateAPIView):
    serializer_class = FamousLikeSerializer
    queryset = FamousLike.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    # post 요청시 좋아요 생성 또는 삭제
    def create(self, request, *args, **kwargs):
        try:
            famous_line = FamousLine.objects.get(pk=kwargs['pk'])
        except:
            raise NotAcceptable('명대사가 존재하지 않습니다.')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        famous_like_exist = FamousLike.objects.filter(user=request.user, famous_line=famous_line)
        if famous_like_exist.exists():
            famous_like_exist.delete()
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)
        serializer.save(famous_line=famous_line, user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TopFamousView(APIView):
    # django Aggregation API 활용
    # 참조: https://docs.djangoproject.com/en/1.10/topics/db/aggregation/
    def get(self, request, *args, **kwargs):
        famous_lines = FamousLine.objects.filter(movie=self.kwargs['pk'])
        top_comment = famous_lines.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:3]
        serializer = FamousLineSerializer(top_comment, many=True)
        return Response(serializer.data)
