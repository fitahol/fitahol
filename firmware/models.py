# coding=utf-8
from django.db import models
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class Feedback(models.Model):
    nickname = models.CharField("昵称", max_length=16)
    contact = models.CharField("联系方式", max_length=100)
    content = models.CharField("反馈内容", max_length=1000)
    ctime = models.DateTimeField("创建时间", auto_now=True)

    class Meta:
        db_table = "feedback"
        verbose_name = "用户反馈"
        verbose_name_plural = "用户反馈"

    def __str__(self):
        return self.nickname
    
CLIENT_STATE_CHOICES = (
    (1, u"上线"),
    (0, u"下线"),
)

CLIENT_PlAT_CHOICES = (
    (0, u"Android"),
    (1, u"iOS"),
)


class ClientVersion(models.Model):
    platform = models.SmallIntegerField("所属平台", choices=CLIENT_PlAT_CHOICES,
                                        default=0)
    start_version = models.CharField("开始版本号", max_length=6, default="1.0.0",
                                     help_text="版本号必须是 x.x.x 单位数 ")
    end_version = models.CharField("结束版本号", max_length=6)
    version = models.CharField("当前版本", max_length=6)
    desc = models.TextField("升级描述")
    android_url = models.FileField("Android下载地址", upload_to="firmware/version",
                                   blank=True)
    ios_url = models.CharField("Android下载地址", max_length=500,
                               blank=True)
    is_force = models.BooleanField("是否强制升级", default=False)
    state = models.SmallIntegerField(
        u"状态码", choices=CLIENT_STATE_CHOICES,
        db_index=True, default=0)
    ctime = models.DateTimeField(u"创建时间", auto_now_add=True)
    utime = models.DateTimeField(u"更新时间", auto_now=True)

    class Meta:
        db_table = "client_config"
        verbose_name = u"客户端升级配置"
        verbose_name_plural = u"客户端升级升级配置"
