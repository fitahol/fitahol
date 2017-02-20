# coding=utf-8
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from six import python_2_unicode_compatible

import pypinyin

from fitness.models import ExpertTag
from gym.models import Gymnasium
from notifications.signals import notify

MEMBER_TYPE_CHOICES = (
    (-1, "未选择"),
    (0, "学员"),
    (1, "教练"),
)

SEX_CHOICES = (
    (0, u"未知"),
    (1, u"男性"),
    (2, u"女性"),
)

OS_PLATFORM_CHOICES = (
    (0, u'iOS'),
    (1, u'Android'),
    (2, u'unknown'),
    (3, u'iOS7'),
)


@python_2_unicode_compatible
class WechatInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    unionid = models.CharField(u"开放平台唯一ID", max_length=100, blank=True,
                               help_text=u"多帐户绑定同一微信开放平台后,会有这个值")
    openid = models.CharField(u"微信openid", max_length=100, unique=True)
    headimgurl = models.CharField(u"头像", max_length=500, blank=True)
    os_platform = models.SmallIntegerField(u"系统平台", default=2,
                                           choices=OS_PLATFORM_CHOICES)
    nickname = models.CharField(u"微信昵称", max_length=100, blank=True)
    sex = models.SmallIntegerField(u"性别", choices=SEX_CHOICES, default=0)
    city = models.CharField(u"城市名", max_length=16, blank=True)
    province = models.CharField(u"省名", max_length=16, blank=True)
    country = models.CharField(u"国家", max_length=16, blank=True)
    wechat_subscribed = models.BooleanField(u"微信关注", default=False)
    subscribe_time = models.CharField(u"关注时间", max_length=16, blank=True,
                                      help_text=u"值为unix时间截")
    groupid = models.SmallIntegerField(u"微信分组", default=0)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wechat_info'
        verbose_name = '用户微信信息'
        verbose_name_plural = '用户微信信息'

    def __str__(self):
        return self.nickname


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nickname = models.CharField("昵称", max_length=36, blank=True,
                                db_index=True)
    intro = models.CharField("个性签名", max_length=500, default="", blank=True)
    phone = models.CharField("手机号", max_length=16, blank=True, unique=True)
    weight = models.IntegerField("体重", default=0, help_text="单位为千克")
    height = models.IntegerField("身高", default=0, help_text="单位为厘米")
    gender = models.SmallIntegerField(u"性别", choices=SEX_CHOICES, default=0)
    age = models.IntegerField("年龄", default=0)
    u_type = models.SmallIntegerField("用户身份", default=-1,
                                      choices=MEMBER_TYPE_CHOICES)
    score = models.IntegerField("积分", default=0)
    portrait = models.ImageField("头像", upload_to="account/portrait",
                                 blank=True)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profile"
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    def __str__(self):
        return "uid:%s, %s" % (self.user_id, self.nickname)

    @property
    def portrait_url(self):
        if self.portrait:
            return settings.HTTP_SERVER_URL + self.portrait.url
        if hasattr(self.user, "wechatinfo"):
            return self.user.wechatinfo.headimgurl
        if self.gender == 2:
            return "https://api.fitahol.com/media/icon/fitness-girl.png"
        else:
            return "https://api.fitahol.com/media/icon/fitness-boy.png"


@python_2_unicode_compatible
class Figure(models.Model):
    """用户形象墙, 之后可以关联事件"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    figure = models.ImageField("形象照", upload_to="account/figure")
    desc = models.CharField("描述", max_length=200, blank=True)
    cdate = models.DateField("日期", blank=True)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_figure"
        verbose_name = "用户形象"
        verbose_name_plural = "用户形象"
        ordering = ("-id", )

    def __str__(self):
        return self.figure.url


@python_2_unicode_compatible
class Coach(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    experience = models.IntegerField("资历", default=0)
    gym = models.ForeignKey(Gymnasium, blank=True)
    expert_tags = models.ManyToManyField(ExpertTag)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'coach'
        verbose_name = "教练"
        verbose_name_plural = "教练"

    def get_nickname(self):
        return self.user.profile.nickname

    def __str__(self):
        return "ID:%s, %s" % (self.user_id, self.get_nickname())

REF_CHOICES = (
    ("add_member", "添加学员"),
    ("add_coach", "添加教练"),
    ("add_friend", "添加好友"),
    ("add_follow", "添加关注"),
)

CONFIRM_CHOICES = (
    (1, "接受"),
    (-1, "拒绝"),
    (0, "等待回应"),
)


@python_2_unicode_compatible
class UserRelationConfirm(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sender")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='recipient')
    ref_type = models.CharField("关联类型", max_length=16, choices=REF_CHOICES)
    status = models.SmallIntegerField("状态", default=0)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_ref_confirm"
        verbose_name = "用户关联请求"
        verbose_name_plural = "用户关联请求"
        ordering = ("-id", )

    def __str__(self):
        return "绑定[用户%s & 用户%s]关系确认" % (self.sender.id, self.recipient.id)


def user_rel_handler(sender, instance, created, **kwargs):
    description = "教练: %s 请求添加您为学员" % instance.sender.profile.nickname
    title = description
    notify.send(sender=instance.sender, recipient=instance.recipient,
                action_object=instance, show_time=instance.ctime,
                description=description, title=title)

post_save.connect(user_rel_handler, sender=UserRelationConfirm)


@python_2_unicode_compatible
class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    gym = models.ForeignKey(Gymnasium, blank=True, null=True)
    coach = models.ManyToManyField(Coach, blank=True,
                                   through='CoachMemberRef')
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'member'
        verbose_name = "学员"
        verbose_name_plural = "学员"

    def get_nickname(self):
        return self.user.profile.nickname

    def get_portrait(self):
        return self.user.profile.portrait_url
    
    def get_gender(self):
        return self.user.profile.gender

    def pinyin_first_letter(self):
        nickname = self.get_nickname()
        if not nickname:
            return ""
        first_letter_str = pypinyin.lazy_pinyin(
            self.get_nickname(), pypinyin.FIRST_LETTER)[0]
        first_letter = first_letter_str[0]
        if not first_letter.isalpha():
            return "#"
        return first_letter

    def __str__(self):
        return "uid: %s" % self.user_id


class CoachMemberRef(models.Model):
    member = models.ForeignKey(Member)
    coach = models.ForeignKey(Coach)
    primary = models.BooleanField("主教练", default=False)
    
    class Meta:
        db_table = "member_coach"
        unique_together = ("member", "coach")
        verbose_name = "学员教练关联"
        verbose_name_plural = "学员教练关联"


def get_str_render(self):
    return "%s-%s" % (self.id, self.username)

User.add_to_class("__str__", get_str_render)
