from rest_framework.views import APIView
from rest_framework.response import Response
from movie.serializers.magazine import MagazineSerializer
from movie.models import Magazine


class MagazineList(APIView):
    def get(self, request):
        magazine = Magazine.objects.all()
        serializer = MagazineSerializer(magazine, many=True)
        return Response(serializer.data)