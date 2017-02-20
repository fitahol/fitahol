# coding=utf-8
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from schedule.models import Event


@python_2_unicode_compatible
class ExpertTag(models.Model):
    name = models.CharField("名称", max_length=36, unique=True)
    desc = models.CharField("说明", max_length=1000, blank=True)
    is_public = models.BooleanField("全员可见", default=False)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "expert_tags"
        verbose_name = "教练专长领域"
        verbose_name_plural = "教练专长领域"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class FitGoal(models.Model):
    name = models.CharField("目标名称", max_length=20)
    desc = models.CharField("目标描述", max_length=1000, blank=True)
    is_public = models.BooleanField("全员可见", default=False)
    measure = models.CharField("计量单位", max_length=16,
                               default="Kg", help_text="不同类型健身指标不同")
    initial = models.IntegerField("初始值", default=0)
    goal = models.IntegerField("目标值", default=0,
                               help_text="不同类型,指标值不同")
    schedule = models.IntegerField("达成预期天数", default=0,
                                   help_text="按天数计")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fit_goal"
        verbose_name = "健身目标"
        verbose_name_plural = "健身目标"
        unique_together = ("user", "name")
        
    def get_user_info(self):
        return {"user_id": self.user_id,
                "nickname": self.user.profile.nickname,
                "portrait": self.user.profile.portrait_url
                }

    def __str__(self):
        return "%s-%s" % (self.id, self.name)


@python_2_unicode_compatible
class GoalRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    fit_goal = models.ForeignKey(FitGoal)
    current = models.IntegerField("当前值", default=0)
    figure = models.ImageField("晒图", upload_to="fitness/figure", blank=True)
    cdate = models.DateField("日期", db_index=True)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fitness_goal_record"
        verbose_name = "目标更新记录"
        verbose_name_plural = "目标更新记录"
        ordering = ("-cdate", )

    def get_current_desc(self):
        return "%s %s" % (self.current, self.fit_goal.measure)
    
    def get_short_cdate(self):
        return self.cdate.strftime("%m-%d")

    def __str__(self):
        return "uid: %s, goal: %s" % (self.user_id, self.fit_goal)


@python_2_unicode_compatible
class InBodyRecords(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    cdate = models.DateField("日期")
    weight = models.IntegerField("体重", default=0)
    metabolism = models.IntegerField("基础代谢", default=0)
    body_fat = models.IntegerField("体脂率", default=0)
    fat_weight = models.IntegerField("脂肪重量", default=0)
    skeletal_muscle = models.IntegerField("骨骼肌", default=0)
    chest = models.IntegerField("胸围", default=0)
    arm = models.IntegerField("臂围", default=0)
    upper_arm = models.IntegerField("上臂围", default=0)
    waistline = models.IntegerField("腰围", default=0)
    thigh = models.IntegerField("大腿围", default=0)
    crus = models.IntegerField("小腿围", default=0)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "in_body_records"
        verbose_name = "InBody体测机数据记录"
        verbose_name_plural = "InBody体测机数据记录"

    def __str__(self):
        return "date: %s, uid: %s" % (self.cdate, self.user_id)


@python_2_unicode_compatible
class FitnessPicture(models.Model):
    picture = models.ImageField("配图", upload_to="gym/pictures")
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "fitness_pictures"
        verbose_name = "健身配图"
        verbose_name_plural = "健身配图"

    def __str__(self):
        return self.picture.url


@python_2_unicode_compatible
class FitnessVideo(models.Model):
    video = models.ImageField("视频", upload_to="gym/videos")
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "fitness_videos"
        verbose_name = "健身视频"
        verbose_name_plural = "健身视频"

    def __str__(self):
        return self.video.url


@python_2_unicode_compatible
class FitnessEquipment(models.Model):
    name = models.CharField("名称", max_length=50)
    desc = models.CharField("作用描述", max_length=500, blank=True)
    cover = models.ImageField("封面", upload_to="gym/equipment",
                              blank=True, null=True)
    pictures = models.ManyToManyField(FitnessPicture, blank=True)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fitness_equipment"
        verbose_name = "健身设备"
        verbose_name_plural = "健身设备"

    def __str__(self):
        return "%s: %s" % (self.id, self.name)


@python_2_unicode_compatible
class ExerciseCategory(models.Model):
    name = models.CharField("中文名称", max_length=50)
    en_name = models.CharField("英文名称", max_length=500, blank=True)
    icon = models.ImageField("图标", upload_to="gym/icons", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             help_text="用户自定义, 默认对其他人不可见")
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fitness_category"
        verbose_name = "健身大类目"
        verbose_name_plural = "健身大类目"

    def __str__(self):
        return "%s: %s" % (self.id, self.name)


class Muscle(models.Model):
    name = models.CharField("中文名称", max_length=50)
    en_name = models.CharField("英文名称", max_length=500, blank=True)
    image = models.ImageField("示例图片", upload_to="gym/muscle", blank=True)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fitness_muscle"
        verbose_name = "肌群分类"
        verbose_name_plural = "肌群分类"

    def get_muscle_level(self, user):
        return ExerciseMuscle.objects.get(muscle=self, )


MUSCLE_LEVEL_CHOICES = (
    ("primary", "主肌群"),
    ("secondary", "附肌群"),
)


class ExerciseMuscle(models.Model):
    muscle = models.ForeignKey(Muscle)
    exercise = models.ForeignKey('FitnessExercise')
    level = models.CharField(
        "肌群级别", default="primary", max_length=16,
        choices=MUSCLE_LEVEL_CHOICES,
        help_text="一般健身动作包括主肌群和附肌群锻炼; "
                  "主肌群示例图片为红色值为primary, "
                  "附肌群为蓝色示例图片, 值为secondary")
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "exercise_muscle_ref"
        verbose_name = "肌群动作关联表"
        verbose_name_plural = "肌群动作关联表"

    def get_muscle_name(self):
        return self.muscle.name

    def get_muscle_image(self):
        return self.muscle.image.url


@python_2_unicode_compatible
class FitnessExercise(models.Model):
    name = models.CharField("名称", max_length=50, db_index=True)
    pinyin = models.CharField("拼音名称", max_length=100, blank=True,
                              db_index=True)
    en_name = models.CharField("英文名称", max_length=500, blank=True)
    desc = models.TextField("描述", blank=True)
    category = models.ForeignKey(ExerciseCategory, verbose_name="分类",
                                 db_index=True)
    muscles = models.ManyToManyField(Muscle, through=ExerciseMuscle, blank=True)
    icon = models.ImageField("封面", upload_to="gym/exercise_icon",
                             blank=True, null=True)
    equipment = models.ManyToManyField(FitnessEquipment, blank=True,
                                       verbose_name="使用设备")
    pictures = models.ManyToManyField(FitnessPicture, blank=True,
                                      verbose_name="配图")
    videos = models.ManyToManyField(FitnessVideo, blank=True,
                                    verbose_name="演示视频")
    unit = models.CharField("计量单位", max_length=16, default="KG")
    strength = models.CharField("强度单位", max_length=100,
                                blank=True, help_text="和计量单位搭配, 衡量健身动作")
    is_public = models.BooleanField("是否全员可用", default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             help_text="个人定制")
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fitness_exercise"
        verbose_name = "健身动作"
        verbose_name_plural = "健身动作"
        ordering = ("pinyin", )

    def __str__(self):
        return "%s: %s" % (self.id, self.name)
    
    def get_first_letter(self):
        return self.pinyin[0]

    def get_icon_url(self):
        if self.icon:
            return settings.HTTP_SERVER_URL + self.icon.url
        return ""


@python_2_unicode_compatible
class ExerciseRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    event = models.ForeignKey(Event)
    exercise = models.ForeignKey(FitnessExercise)
    value = models.IntegerField("计量值", default=0)
    number = models.IntegerField("次数", default=0)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fitness_exercise_record"
        verbose_name = "健身动作记录"
        verbose_name_plural = "健身动作记录"
        index_together = ("user", "event")

    def __str__(self):
        return "%s: %s" % (self.value, self.number)
