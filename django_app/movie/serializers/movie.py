from rest_framework import serializers

from movie.models import Movie, MovieImages, Actor, Director, Genre, Grade, MakingCountry, MovieLike, MovieActor

################################################################################
# 감독, 배우 시리얼라이저                                                           #
################################################################################


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
            'id',
            'daum_id',
            'name_kor',
            'name_eng',
            'profile_url',
        )


class CharacterNameSerializer(serializers.ModelSerializer):
    actor = ActorDetailSerializer()

    class Meta:
        model = MovieActor
        fields = ('actor', 'character_name',)

################################################################################
# 영화 이미지, 장르, 관람등급, 국가 시리얼라이저                                          #
################################################################################


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
            'id',
            'content',
        )


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = (
            'id',
            'content',
        )


class MakingCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MakingCountry
        fields = (
            'id',
            'content',
        )

################################################################################
# 영화 시리얼라이저                                                                #
################################################################################


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
            'main_image_url',
            'run_time',
            'star_sum',
            'comment_count',
            'star_average',
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    image_set = MovieImageSerializer(many=True, read_only=True, source='movieimages_set')
    director = DirectorDetailSerializer(many=True, read_only=True)
    actors = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    grade = GradeSerializer(read_only=True)
    making_country = MakingCountrySerializer(many=True, read_only=True)
    star_average = serializers.ReadOnlyField()

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
            'main_image_url',
            'run_time',
            'synopsis',
            'image_set',
            'main_trailer',
            'star_sum',
            'comment_count',
            'star_average',
            'likes_count',
            'like_users',
            'comment_users',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['is_like'] = False
        ret['is_comment'] = False
        request = self.context.get('request')
        if request is not None:
            if request.user.is_authenticated:
                if instance.like_users.filter(id=request.user.pk).exists():
                    ret['is_like'] = True
                if instance.comment_users.filter(id=request.user.pk).exists():
                    ret['is_comment'] = True
        return ret

    def get_actors(self, obj):
        actors = MovieActor.objects.filter(movie=obj.pk).order_by('id')
        serializers = CharacterNameSerializer(actors, many=True)
        return serializers.data


################################################################################
# 영화 좋아요 시리얼라이저                                                           #
################################################################################


class MovieLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MovieLike
        fields = ('user', )


class MovieMyLikeSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = MovieLike
        fields = ('movie', )

################################################################################
# 박스오피스 시리얼라이저                                                            #
################################################################################


class BoxOfficeDetailSerializer(serializers.ModelSerializer):
    image_set = MovieImageSerializer(many=True, read_only=True, source='movieimages_set')
    genre = GenreSerializer(many=True, read_only=True)
    grade = GradeSerializer(read_only=True)
    making_country = MakingCountrySerializer(many=True, read_only=True)
    star_average = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = (
            'id',
            # 'daum_id',
            'title_kor',
            'title_eng',
            'genre',
            # 'director',
            # 'actors',
            'grade',
            'making_country',
            # 'created_year',
            'img_url',
            'main_image_url',
            'run_time',
            # 'synopsis',
            'image_set',
            'main_trailer',
            # 'star_sum',
            # 'comment_count',
            'star_average',
            # 'likes_count',
            # 'like_users',
            # 'comment_users',
        )


class BoxOfficeDetailSerializerIOS(serializers.ModelSerializer):
    """
    IOS 용 박스오피스입니다.
    """
    grade = GradeSerializer(read_only=True)
    star_average = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'grade',
            'img_url',
            'star_average',
        )

################################################################################
# 연관영화 시리얼라이저                                                             #
################################################################################


class RelatedMovieSerializer(serializers.ModelSerializer):
    star_average = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'title_kor',
            'title_eng',
            'img_url',
            'star_average',
        )
