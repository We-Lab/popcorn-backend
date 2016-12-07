from rest_framework import serializers
from member.models import MyUser
from movie.models import Movie, MovieImages, Actor, Director, Comment, FamousLine


# from movie.serializers.famous_line import FamousLineSerializer


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = (
            'name_kor',
            'name_eng',
        )


class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = (
            'daum_id',
            'name_kor',
            'name_eng',
            'profile_url',
        )


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = (
            'name_kor',
            'name_eng',
        )


class ActorDetailSerializer(serializers.ModelSerializer):
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
            'id',
            'movie',
            'url',
        )


class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='genre'
    )
    grade = serializers.SlugRelatedField(
        read_only=True,
        slug_field='grade',
    )

    class Meta:
        model = Movie
        fields = (
            'id',
            'daum_id',
            'title_kor',
            'title_eng',
            'genre',
            'director',
            'actors',
            'grade',
            'created_year',
            'img_url',
            'run_time',
            'star_sum',
            'comment_count',
            'star_average',
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    image_set = MovieImageSerializer(many=True, read_only=True, source='movieimages_set')
    director = DirectorDetailSerializer(many=True, read_only=True)
    actors = ActorDetailSerializer(many=True, read_only=True)
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='genre'
    )
    grade = serializers.SlugRelatedField(
        read_only=True,
        slug_field='grade',
    )
    star_average = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = (
            'daum_id',
            'title_kor',
            'title_eng',
            'genre',
            'director',
            'actors',
            'grade',
            'created_year',
            'img_url',
            'run_time',
            'synopsis',
            'image_set',
            'main_trailer',
            'star_sum',
            'comment_count',
            'star_average',
        )
