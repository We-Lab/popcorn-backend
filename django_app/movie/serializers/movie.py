from rest_framework import serializers
from movie.models import Movie, MovieImages, Actor


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = (
            'daum_id',
            'name_kor',
            'name_eng',
            'profile_url',
        )


class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieImages
        fields = (
            # 'movie',
            'url',
        )


class MovieSerializer(serializers.ModelSerializer):
    # actor_list = ActorSerializer(many=True, source='actor_set')

    class Meta:
        model = Movie
        fields = (
            'daum_id',
            'title_kor',
            'title_eng',
            'genre',
            'actors',
            'director',
            'grade',
            'created_year',
            'img_url',
            'run_time',
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    image_set = MovieImageSerializer(many=True, source='movieimages_set')

    class Meta:
        model = Movie
        fields = (
            'daum_id',
            'title_kor',
            'title_eng',
            'genre',
            'actors',
            'director',
            'grade',
            'created_year',
            'img_url',
            'run_time',
            'synopsis',
            'image_set',
        )