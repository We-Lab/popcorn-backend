""" 영화 serializer module
영화 관련된 정보를 직렬화 합니다.
대부분 기본정보와 상세정보 두 가지로 직렬화합니다.
"""
from rest_framework import serializers

from movie.models import Movie, MovieImages, Actor, Director, Genre, Grade, MakingCountry, MovieLike, MovieActor


class DirectorSerializer(serializers.ModelSerializer):
    """
    감독정보 직렬화
    """
    class Meta:
        model = Director
        fields = (
            'name_kor',
            'name_eng',
        )


class DirectorDetailSerializer(serializers.ModelSerializer):
    """
    감독 상세정보 직렬화
    """
    class Meta:
        model = Director
        fields = (
            'daum_id',
            'name_kor',
            'name_eng',
            'profile_url',
        )


class ActorSerializer(serializers.ModelSerializer):
    """
    배우정보 직렬화
    """
    class Meta:
        model = Actor
        fields = (
            'name_kor',
            'name_eng',
        )


class ActorDetailSerializer(serializers.ModelSerializer):
    """
    배우 상세정보 직렬화
    """
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
    """
    배우 역할명 직렬화
    배우정보 nested
    """
    actor = ActorDetailSerializer()

    class Meta:
        model = MovieActor
        fields = ('actor', 'character_name',)


class MovieImageSerializer(serializers.ModelSerializer):
    """
    영화 기타 이미지 직렬화
    """
    class Meta:
        model = MovieImages
        fields = (
            'id',
            'movie',
            'url',
        )


class GenreSerializer(serializers.ModelSerializer):
    """
    장르 직렬화
    """
    class Meta:
        model = Genre
        fields = (
            'id',
            'content',
        )


class GradeSerializer(serializers.ModelSerializer):
    """
    관람등급 직렬화
    """
    class Meta:
        model = Grade
        fields = (
            'id',
            'content',
        )


class MakingCountrySerializer(serializers.ModelSerializer):
    """
    제작국가 직렬화
    """
    class Meta:
        model = MakingCountry
        fields = (
            'id',
            'content',
        )


class MovieSerializer(serializers.ModelSerializer):
    """
    영화 기본 직렬화
    감독, 배우, 장르, 관람등급, 제작국가 nested
    """
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

    # 영화 좋아요 작성여부, 댓글 작성여부 추가
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


class MovieDetailSerializer(serializers.ModelSerializer):
    """
    영화 상세정보 직렬화
    기타 영화이미지, 감독, 배우, 장르, 관람등급, 제작국가 neasted
    serializer method로 배우정보(캐릭터 이름 포함) 추가
    """
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

    # 영화 좋아요 작성여부, 댓글 작성여부 추가
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

    # 캐릭터 이름 포함하여 배우정보 nested
    def get_actors(self, obj):
        actors = MovieActor.objects.filter(movie=obj.pk).order_by('id')
        serializers = CharacterNameSerializer(actors, many=True)
        return serializers.data


class MovieLikeSerializer(serializers.ModelSerializer):
    """
    영화 좋아요 직렬화
    """
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MovieLike
        fields = ('user', )


class MovieMyLikeSerializer(serializers.ModelSerializer):
    """
    유저가 좋아요한 영화 직렬화
    영화정보 nested
    """
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = MovieLike
        fields = ('movie', )


class BoxOfficeDetailSerializer(serializers.ModelSerializer):
    """
    박스오피스 상세정보 직렬화
    기타 영화 이미지, 장르, 관람등급, 제작국가 nested
    """
    image_set = MovieImageSerializer(many=True, read_only=True, source='movieimages_set')
    genre = GenreSerializer(many=True, read_only=True)
    grade = GradeSerializer(read_only=True)
    making_country = MakingCountrySerializer(many=True, read_only=True)
    star_average = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'title_kor',
            'title_eng',
            'genre',
            'grade',
            'making_country',
            'img_url',
            'main_image_url',
            'run_time',
            'image_set',
            'main_trailer',
            'star_average',
        )


class BoxOfficeDetailSerializerIOS(serializers.ModelSerializer):
    """
    박스오피스 상세정보 직렬화 ios 전용
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


class RelatedMovieSerializer(serializers.ModelSerializer):
    """
    관련영화 직렬화
    """
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
