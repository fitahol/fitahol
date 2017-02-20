# coding=utf-8
from django.contrib import admin

from gym.models import Country, City, Province, District, Gymnasium


class CountryAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "languages", "capital")

admin.site.register(Country, CountryAdmin)


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("code", "pcode", "name", "suffix", "fullname", "pinyin")
    search_fields = ("code", "name", "fullname")

admin.site.register(Province, ProvinceAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ("code", "pcode", "name", "suffix", "fullname", "pinyin")
    search_fields = ("code", "name", "fullname", "pcode__name")

admin.site.register(City, CityAdmin)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ("code", "pcode", "name", "suffix", "fullname", "pinyin")
    search_fields = ("code", "name", "fullname")

admin.site.register(District, DistrictAdmin)


class GymnasiumAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city_code", "district_code", "address",
                    "telephone", "ctime")
    search_fields = ("name", "address")
    raw_id_fields = ("city_code", "district_code")

admin.site.register(Gymnasium, GymnasiumAdmin)
