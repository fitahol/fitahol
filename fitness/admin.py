# coding=utf-8
from django.contrib import admin
from django.template.defaultfilters import truncatechars_html

from fitness.models import GoalRecord, InBodyRecords, FitGoal
from fitness.models import FitnessEquipment, FitnessExercise, FitnessPicture, \
    FitnessVideo, ExerciseCategory, Muscle, ExerciseRecord


class GoalRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "cdate", "fit_goal", "current", "ctime")

admin.site.register(GoalRecord, GoalRecordAdmin)


class InBodyRecordsAdmin(admin.ModelAdmin):
    list_display = ("id", "cdate", "weight", "metabolism", "body_fat",
                    "fat_weight", "skeletal_muscle", "chest", "arm",
                    "upper_arm", "waistline", "thigh", "crus")

admin.site.register(InBodyRecords, InBodyRecordsAdmin)


class FitnessEquipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "desc", "ctime")

admin.site.register(FitnessEquipment, FitnessEquipmentAdmin)


class FitnessExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "icon_img", "cut_desc", "category", "ctime")
    search_fields = ("name", "desc")
    list_filter = ("category", )

    def cut_desc(self, obj):
        return truncatechars_html(obj.desc, 30)

    cut_desc.short_description = u'内容介绍'
    cut_desc.allow_tags = True

    def icon_img(self, obj):
        return '<img src="%s" alt="icon img" />' % obj.icon.url

    icon_img.short_description = u"封面图标"
    icon_img.allow_tags = True

admin.site.register(FitnessExercise, FitnessExerciseAdmin)


class FitnessPictureAdmin(admin.ModelAdmin):
    list_display = ("id", "picture", "ctime")

admin.site.register(FitnessPicture, FitnessPictureAdmin)


class FitnessVideoAdmin(admin.ModelAdmin):
    list_display = ("id", "video", "ctime")

admin.site.register(FitnessVideo, FitnessVideoAdmin)


class MuscleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "en_name", "image_show")

    def image_show(self, obj):
        return '<img src="%s" alt="icon img" width="100px" />' % obj.image.url

    image_show.short_description = u"封面图标"
    image_show.allow_tags = True

admin.site.register(Muscle, MuscleAdmin)


class ExerciseCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "en_name", "icon", "user", "ctime")

admin.site.register(ExerciseCategory, ExerciseCategoryAdmin)


class FitGoalAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "desc", "is_public", "goal", "ctime")

admin.site.register(FitGoal, FitGoalAdmin)


class ExerciseRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "event", "exercise", "value", "number", "ctime")
    
admin.site.register(ExerciseRecord, ExerciseRecordAdmin)
