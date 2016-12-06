from rest_framework import serializers
from member.models import MyUser
from movie.models import Movie, MovieImages, Actor, Director, Comment, FamousLine


# from movie.serializers.famous_line import FamousLineSerializer


class MovieIdTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id',
            'title_kor',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    # like_users 필드로 사용자의 좋아요 선택여부 판단 가능
    class Meta:
        model = Comment
        fields = (
            'id',
            'movie',
            'movie_title',
            'author',
            'star',
            'content',
            'likes_count',
            'like_users',
            'created_date',
        )


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


class FamousLineSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FamousLine
        fields = (
            'id',
            'movie',
            'movie_title',
            'actor',
            'actor_kor_name',
            'actor_character_name',
            'author',
            'content',
            'likes_count',
            'like_users',
            'created_date',
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
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    image_set = MovieImageSerializer(many=True, read_only=True, source='movieimages_set')
    director = DirectorDetailSerializer(many=True, read_only=True)
    actors = ActorDetailSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    famous_lines = FamousLineSerializer(many=True, read_only=True, source='famousline_set')
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
            'comments',
            'famous_lines',
            'main_trailer',
            'star_average',
        )
