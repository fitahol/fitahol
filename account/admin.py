# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from account.models import Profile, Member, Coach, Figure, ExpertTag, \
    UserRelationConfirm, CoachMemberRef, WechatInfo

admin.site.site_header = 'fitahol'


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'uid', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)

    def uid(self, obj):
        return obj.user.id
    uid.short_description = u'用户ID'

admin.site.unregister(Token)
admin.site.register(Token, TokenAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserCustomAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff')
    inlines = (ProfileInline, )
    ordering = ('-id', )

admin.site.unregister(User)
admin.site.register(User, UserCustomAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("uid", "user", "portrait_img", "u_type", "nickname", "phone",
                    "gender", "age", "ctime")

    def uid(self, obj):
        return obj.user.id
    
    def portrait_img(self, obj):
        return '<img src="%s" width="50px" alt="portrait icon" />' % obj.portrait_url

    uid.short_description = u'用户ID'
    portrait_img.short_description = u"图标"
    portrait_img.allow_tags = True

admin.site.register(Profile, ProfileAdmin)


class CoachMemberRefAdmin(admin.ModelAdmin):
    list_display = ("id", "member", "coach", "primary")
    list_filter = ("primary", )
    search_fields = ("=member__user__id", "=coach__user__id")

admin.site.register(CoachMemberRef, CoachMemberRefAdmin)


class CoachAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "experience",
                    "expert_tags_list", "ctime")

    def expert_tags_list(self, obj):
        return "<br />".join([each.name for each in obj.expert_tags.all()])
    expert_tags_list.short_description = "擅长领域"
    expert_tags_list.allow_tags = True

admin.site.register(Coach, CoachAdmin)


class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "uid", "user",
                    "gym", "ctime")

    def uid(self, obj):
        return obj.user.id
    uid.short_description = u'用户ID'

admin.site.register(Member, MemberAdmin)


class UserRelationConfirmAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "recipient", "status", "ctime")
    
admin.site.register(UserRelationConfirm, UserRelationConfirmAdmin)


class FigureAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "figure", "cdate", "ctime")

admin.site.register(Figure, FigureAdmin)


class ExpertTagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "desc", "is_public", "ctime")

admin.site.register(ExpertTag, ExpertTagAdmin)


class WechatInfoAdmin(admin.ModelAdmin):
    list_display = ("uid", "nickname", "user", "openid", "ctime")
    
    def uid(self, obj):
        return obj.user.id
    uid.short_description = u'用户ID'
    
admin.site.register(WechatInfo, WechatInfoAdmin)
