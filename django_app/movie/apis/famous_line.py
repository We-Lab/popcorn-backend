""" 명대사 view module
1. 해당 영화의 배우를 선택해서 명대사를 기입할 수 있습니다.
2. 명대사는 유저가 복수 등록 가능합니다.
3. 좋아요 기능이 있습니다.
"""
from django.db.models import Count
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import MyUser
from movie.models import FamousLine, Movie, Actor, FamousLike
from movie.permissions import IsOwnerOrReadOnly
from movie.serializers.famous_line import FamousLineSerializer, FamousLikeSerializer
from mysite.utils.profanities_filter import ProfanitiesFilter


class FamousLiseView(generics.ListCreateAPIView):
    """
    명대사 리스트, 생성
    """
    serializer_class = FamousLineSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CursorPagination

    def get_queryset(self):
        movie_pk = self.kwargs['pk']
        # print(movie_pk)
        return FamousLine.objects.filter(movie=movie_pk)

    def perform_create(self, serializer):
        """
        1. 욕설 필터링 사용
        2. 유저가 복수의 명대사를 작성 가능
        3. 해당영화의 배우인지 확인
        """
        # print(self)
        movie_pk = self.kwargs['pk']
        movie = Movie.objects.get(pk=movie_pk)
        author = MyUser.objects.get(pk=self.request.user.id)
        a1 = Actor.objects.filter(movie=movie_pk)
        a2 = Actor.objects.get(pk=self.request.data['actor'])

        # 해당 영화의 배우인지 확인
        if a2 not in [i for i in a1]:
            raise ParseError('해당 배우를 찾을 수 없습니다.')

        # 욕설 필터링
        content = self.request.data['content']
        r = ProfanitiesFilter()
        clean_content = r.clean(content)

        serializer.save(movie=movie, actor=a2, author=author, content=clean_content)


class FamousLineDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    명대사 상세
    """
    serializer_class = FamousLineSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = FamousLine.objects.all()

    def perform_update(self, serializer):
        """
        1. 욕설 필터링 사용
        2. 해당영화의 배우인지 확인
        """
        famous_pk = self.kwargs['pk']  # get object 기본이 pk라 url 키워드 다 movie_pk -> pk로 변경함
        famous_line = FamousLine.objects.get(pk=famous_pk)
        movie_pk = famous_line.movie.pk
        actors = Actor.objects.filter(movie=movie_pk)
        actor = Actor.objects.get(pk=self.request.data['actor'])

        # 욕설 필터링
        try:
            content = self.request.data['content']
            r = ProfanitiesFilter()
            clean_content = r.clean(content)
        except:
            clean_content = serializer.instance.content

        # 해당 영화의 배우인지 확인
        if actor not in [i for i in actors]:
            raise ParseError('해당 배우를 찾을 수 없습니다.')

        serializer.save(content=clean_content)


class FamousLikeView(generics.CreateAPIView):
    """
    명대사 좋아요
    """
    serializer_class = FamousLikeSerializer
    queryset = FamousLike.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        """
        1차 post 요청 좋아요 생성, 2차 post 요청 좋아요 삭제
        """
        try:
            famous_line = FamousLine.objects.get(pk=kwargs['pk'])
        except:
            raise NotFound('명대사가 존재하지 않습니다.')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 중복 요청시 좋아요 삭제
        famous_like_exist = FamousLike.objects.filter(user=request.user, famous_line=famous_line)
        if famous_like_exist.exists():
            famous_like_exist.delete()
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)

        serializer.save(famous_line=famous_line, user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TopFamousView(APIView):
    """
    해당영화 명대사 중 좋아요 개수 상위 3개 출력
    """
    def get(self, request, *args, **kwargs):
        famous_lines = FamousLine.objects.filter(movie=self.kwargs['pk'])
        top_comment = famous_lines.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:3]
        serializer = FamousLineSerializer(top_comment, many=True)
        return Response(serializer.data)
