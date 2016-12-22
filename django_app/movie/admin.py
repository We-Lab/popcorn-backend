from django.contrib import admin

from movie.models import Movie, MovieActor, Comment, FamousLine, BoxOfficeMovie, Magazine


class ActorInline(admin.TabularInline):
    model = MovieActor
    extra = 0


class MovieAdmin(admin.ModelAdmin):
    """
    1. 영화 관리 어드민
    2. 배우 정보 nested
    """
    fieldsets = [
        ('영화 기본정보', {'fields': ['daum_id', 'title_kor', 'title_eng', 'director', 'created_year', 'genre', 'making_country', 'grade', 'run_time']}),
        ('영화 상세정보',
         {'fields': ['synopsis', 'main_image_url', 'img_url', 'main_trailer'], 'classes': ['collapse']}),
        ('영화 평점', {'fields': ['star_sum', 'comment_count', 'star_average']}),
        ('유저 리스트', {'fields': ['like_users', 'comment_users']}),
    ]
    readonly_fields = ['daum_id', 'star_average', 'star_sum', 'comment_count', 'like_users', 'comment_users']
    inlines = (ActorInline, )
    list_display = ('title_kor', 'title_eng', 'created_year', 'created')
    list_filter = ['genre', 'making_country', 'grade']
    search_fields = ['title_kor']
    list_per_page = 10

admin.site.register(Movie, MovieAdmin)


class CommentAdmin(admin.ModelAdmin):
    """
    댓글 정보 어드민
    """
    fields = [
        'author',
        'movie',
        'star',
        'content',
        'like_users',
    ]
    readonly_fields = [
        'like_users',
    ]
    list_display = ('author', 'movie', 'star', 'content', 'created')
    search_fields = ['author__nickname', 'movie__title_kor', 'content']
    list_filter = ['star']
    list_per_page = 10

admin.site.register(Comment, CommentAdmin)


class FamousLineAdmin(admin.ModelAdmin):
    """
    명대사 관리 어드민
    """
    fields = [
        'author',
        'movie',
        'actor',
        'content',
        'like_users',
    ]
    readonly_fields = [
        'like_users',
    ]
    list_display = ('author', 'movie', 'actor', 'actor_character_name', 'content', 'created')
    search_fields = ['author__nickname', 'movie__title_kor', 'content']
    list_per_page = 10

admin.site.register(FamousLine, FamousLineAdmin)


class BoxOfficeAdmin(admin.ModelAdmin):
    """
    박스오피스 관리 어드민
    """
    fields = [
        'rank',
        'movie',
        'release_date',
        'ticketing_rate',
    ]
    list_display = ('rank', 'movie', 'release_date', 'ticketing_rate', 'created')
    list_per_page = 10

admin.site.register(BoxOfficeMovie, BoxOfficeAdmin)


class MagazineAdmin(admin.ModelAdmin):
    """
    매거진 관리 어드민
    """
    fields = [
        'mag_id',
        'title',
        'content',
        'img_url',
    ]
    list_display = ('title', 'created')
    search_fields = ('mag_id', 'title')
    list_per_page = 10

admin.site.register(Magazine, MagazineAdmin)
