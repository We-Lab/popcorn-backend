from django.contrib import admin

from member.models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    """
    유저정보 관리자 어드민
    """
    fieldsets = [
        ('기본정보', {'fields': ['username', 'nickname', 'email', 'gender', 'date_of_birth', 'date_joined']}),
        ('취향정보', {'fields': ['favorite_genre', 'favorite_grade', 'favorite_making_country']}),
    ]
    list_display = ('username', 'nickname', 'email', 'gender', 'date_joined')
    readonly_fields = ('date_joined',)
    list_per_page = 10

admin.site.register(MyUser, MyUserAdmin)
