from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import FamousLine, Movie
from movie.permissions import IsOwnerOrReadOnly
from movie.serializers.famous_line import FamousLineSerializer


class FamousLineAPIView(APIView):
    def get(self, request, *args, **kwargs):
        famous_line = FamousLine.objects.filter(movie=kwargs.get('movie_id')).order_by('-created_date')
        serializer = FamousLineSerializer(famous_line, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        movie = Movie.objects.get(pk=kwargs.get('movie_id'))
        author = request.user
        serializer = FamousLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FamousLineDetailAPIView(APIView):

    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, movie_id, pk):
        try:
            obj = FamousLine.objects.filter(movie_id=movie_id)[int(pk)-1]
            self.check_object_permissions(self.request, obj)
            return obj
        except FamousLine.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        famous_line = self.get_object(movie_id=kwargs.get('movie_id'), pk=kwargs.get('pk'))
        serializer = FamousLineSerializer(famous_line)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        famous_line = self.get_object(movie_id=kwargs.get('movie_id'), pk=kwargs.get('pk'))
        serializer = FamousLineSerializer(famous_line, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        famous_line = self.get_object(movie_id=kwargs.get('movie_id'), pk=kwargs.get('pk'))
        famous_line.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
