from rest_framework import serializers

from movie.models import Movie


class MovieFastLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = (
            'id',
            'title_kor',
            'img_url',
            'created_year',
        )
