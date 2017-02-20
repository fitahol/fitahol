# coding=utf-8
from django.conf import settings
from django.db import models
from six import python_2_unicode_compatible


@python_2_unicode_compatible
class Country(models.Model):
    code = models.CharField("国家代号", max_length=6, primary_key=True,
                            help_text="省级行政区划代码 See  http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201504/t20150415_712722.html")
    name = models.CharField(max_length=50, null=True)
    languages = models.CharField(max_length=250, blank=True, null=True)
    capital = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'c_country'
        verbose_name = "国家"
        verbose_name_plural = "国家"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Province(models.Model):
    code = models.CharField("省代号", max_length=6, primary_key=True,
                            help_text="省级行政区划代码 See  http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201504/t20150415_712722.html")
    pcode = models.ForeignKey(Country, to_field='code', db_column='pcode')
    name = models.CharField("行政区名称", max_length=50)
    suffix = models.CharField("行政单位", max_length=8)
    fullname = models.CharField("全名", max_length=16)
    pinyin = models.CharField("拼音", max_length=32)
    py = models.CharField("简拼", max_length=4,
                          help_text="列pinyin的简拼序列。如beijing:bj")

    class Meta:
        db_table = "c_province"
        verbose_name = "省列表"
        verbose_name_plural = "省列表"

    def __str__(self):
        return "%s-%s" % (self.code, self.name)


@python_2_unicode_compatible
class City(models.Model):
    code = models.CharField("城市代号", max_length=6, primary_key=True,
                            help_text="省级行政区划代码 See  http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201504/t20150415_712722.html")
    pcode = models.ForeignKey(Province, to_field='code', db_column='pcode')
    name = models.CharField("行政区名称", max_length=50)
    suffix = models.CharField("行政单位", max_length=8)
    fullname = models.CharField("全名", max_length=16)
    pinyin = models.CharField("拼音", max_length=32)
    py = models.CharField("简拼", max_length=4,
                          help_text="列pinyin的简拼序列。如beijing:bj")

    class Meta:
        db_table = "c_cities"
        verbose_name = "城市列表"
        verbose_name_plural = "城市列表"

    def __str__(self):
        return "%s-%s" % (self.code, self.name)


@python_2_unicode_compatible
class District(models.Model):
    code = models.CharField("城市代号", max_length=6, primary_key=True,
                            help_text="省级行政区划代码 See  http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201504/t20150415_712722.html")
    pcode = models.ForeignKey(City, to_field='code', db_column='pcode')
    name = models.CharField("行政区名称", max_length=50)
    suffix = models.CharField("行政单位", max_length=8)
    fullname = models.CharField("全名", max_length=16)
    pinyin = models.CharField("拼音", max_length=32)
    py = models.CharField("简拼", max_length=4,
                          help_text="列pinyin的简拼序列。如beijing:bj")

    class Meta:
        db_table = 'c_district'
        verbose_name = '城区信息'
        verbose_name_plural = '城区信息'

    def __str__(self):
        return "%s-%s" % (self.code, self.name)


@python_2_unicode_compatible
class Gymnasium(models.Model):
    """健身房信息"""
    name = models.CharField("名称", max_length=200)
    score = models.IntegerField("评分", default=0)
    address = models.CharField("具体位置", max_length=500, blank=True)
    telephone = models.CharField("联系电话", max_length=100, blank=True,
                                 help_text="多个手机号以,号间隔")
    lat = models.FloatField("纬度", default=0)
    lng = models.FloatField("经度", default=0)
    city_code = models.ForeignKey(City, blank=True, to_field='code',
                                  db_column="city_code")
    district_code = models.ForeignKey(District, to_field='code', blank=True,
                                      db_column='district_code')
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "c_gymnasium"
        unique_together = ("city_code", "district_code", "name")
        verbose_name = "健身房"
        verbose_name_plural = "健身房"

    def __str__(self):
        return self.name

    @property
    def parent(self):
        return self.city

    @property
    def hierarchy(self):
        """Get hierarchy, root first"""
        h_list = self.parent.hierarchy if self.parent else []
        h_list.append(self)
        return h_list
    
    def full_city_info(self):
        return {
                "province": {"code": self.city_code.pcode.code,
                             "name": self.city_code.pcode.name,
                             "fullname": self.city_code.pcode.fullname},
                "city": {"code": self.city_code.code,
                         "name": self.city_code.name,
                         "fullname": self.city_code.fullname},
                "district": {"code": self.district_code.code,
                             "name": self.district_code.name,
                             "fullname": self.district_code.fullname}
                }

    def get_absolute_url(self):
        return "/".join([place.slug for place in self.hierarchy])
