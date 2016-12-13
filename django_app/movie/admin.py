from django.contrib import admin

from movie.models import Movie, MovieActor


class ActorInline(admin.TabularInline):
    model = MovieActor
    extra = 0


class MovieAdmin(admin.ModelAdmin):
    fieldsets = [
        ('영화 기본정보', {'fields': ['daum_id', 'title_kor', 'title_eng', 'director', 'created_year', 'genre', 'making_country', 'grade', 'run_time']}),
        ('영화 상세정보',
         {'fields': ['synopsis', 'main_image_url', 'img_url', 'main_trailer'], 'classes': ['collapse']}),
        ('영화 평점', {'fields': ['star_sum', 'comment_count', 'star_average']}),
        ('유저 리스트', {'fields': ['like_users', 'comment_users']}),
    ]
    readonly_fields = ['daum_id', 'star_average', 'star_sum', 'comment_count', 'like_users', 'comment_users']
    inlines = (ActorInline, )
    list_display = ('title_kor', 'title_eng', 'created_year')
    list_filter = ['genre', 'making_country', 'grade']
    search_fields = ['title_kor']

admin.site.register(Movie, MovieAdmin)
