from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import BoxOfficeMovie
from movie.serializers.box_office import BoxOfficeSerialize


class BoxOfficeAPIView(APIView):

    # 최근에 업데이트된 탑 20위 박스오피스 노출함
    def get(self, request, *args, **kwargs):
        box_office_reversed = BoxOfficeMovie.objects.all().order_by('-created_date')[:10]
        box_office = reversed(box_office_reversed)
        serializer = BoxOfficeSerialize(box_office, many=True)
        return Response(serializer.data)
