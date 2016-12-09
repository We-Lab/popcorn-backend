from rest_framework import serializers
from member.models import MyUser
from movie.models import Movie, MovieImages, Actor, Director, Comment, FamousLine, Genre, Grade, MakingCountry, \
    MovieLike


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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'pk',
            'genre',
        )


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = (
            'pk',
            'grade',
        )


class MakingCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MakingCountry
        fields = (
            'pk',
            'making_country',
        )

class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    grade = GradeSerializer(read_only=True)
    making_country = MakingCountrySerializer(many=True, read_only=True)

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
            'making_country',
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
    genre = GenreSerializer(many=True, read_only=True)
    grade = GradeSerializer(read_only=True)
    making_country = MakingCountrySerializer(many=True, read_only=True)
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
            'making_country',
            'created_year',
            'img_url',
            'run_time',
            'synopsis',
            'image_set',
            'main_trailer',
            'star_sum',
            'comment_count',
            'star_average',
            'likes_count',
            'like_users',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['is_like'] = False
        request = self.context.get('request')
        if request is not None:
            if request.user.is_authenticated:
                if instance.like_users.filter(id=request.user.pk).exists():
                    ret['is_like'] = True
        return ret


class MovieLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MovieLike
        fields = ('user', )