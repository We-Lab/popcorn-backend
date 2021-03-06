from rest_framework import serializers

from movie.models import Magazine


class MagazineSerializer(serializers.ModelSerializer):
    """
    매거진 직렬화
    """
    class Meta:
        model = Magazine
        fields = (
            'id',
            'mag_id',
            'title',
            'content',
            'img_url',
        )