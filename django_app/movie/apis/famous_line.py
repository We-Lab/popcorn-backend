from django.db.models import Count
from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import FamousLine, Movie, Actor, FamousLike
from movie.permissions import IsOwnerOrReadOnly
from movie.serializers.famous_line import FamousLineSerializer, FamousLikeSerializer


class FamousLineAPIView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        famous_line = FamousLine.objects.filter(movie=kwargs.get('movie_id')).order_by('-created_date')
        serializer = FamousLineSerializer(famous_line, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        movie = Movie.objects.get(pk=kwargs.get('movie_id'))
        a1 = Actor.objects.filter(movie__pk=kwargs.get('movie_id'))
        a2 = Actor.objects.get(pk=request.data['actor'])
        if a2 not in [i for i in a1]:
            raise NotAcceptable('해당 배우를 찾을 수 없습니다')
        serializer = FamousLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie, author=request.user, actor=a2)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FamousLineDetailAPIView(APIView):

    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, famous_id):
        try:
            obj = FamousLine.objects.get(id=famous_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except FamousLine.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        famous_line = self.get_object(famous_id=kwargs.get('famous_id'))
        serializer = FamousLineSerializer(famous_line)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        famous_line = self.get_object(famous_id=kwargs.get('famous_id'))
        serializer = FamousLineSerializer(famous_line, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        famous_line = self.get_object(famous_id=kwargs.get('famous_id'))
        famous_line.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FamousLikeView(generics.CreateAPIView):
    serializer_class = FamousLikeSerializer
    queryset = FamousLike.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    # post 요청시 좋아요 생성 또는 삭제
    def create(self, request, *args, **kwargs):
        famous_line = FamousLine.objects.get(pk=kwargs['famous_id'])
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
        top_comment = FamousLine.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:3]
        serializer = FamousLineSerializer(top_comment, many=True)
        return Response(serializer.data)
