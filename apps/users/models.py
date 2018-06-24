from django.db import models
from django.contrib.auth.models import AbstractUser


class ExpertGroup(models.Model):
    name = models.CharField(max_length=20, verbose_name="专家组名称")

    class Meta:
        verbose_name = "专家组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, verbose_name="姓名")
    user_type = models.IntegerField(verbose_name="用户类型", choices=(
        (0, '项目负责人'),
        (1, '管理人员'),
        (2, '专家')
    ), default=0)
    college = models.IntegerField(verbose_name="所属学院", choices=(
        (0, '电子信息学院'),
        (1, '机电工程学院'),
        (2, '计算机学院'),
        (3, '材料与食品学院'),
        (4, '人文社会科学学院'),
        (5, '管理学院'),
        (6, '经贸学院'),
        (7, '外国语学院'),
        (8, '艺术设计学院')
    ), default=0)
    expert_group = models.ForeignKey(ExpertGroup, null=True, blank=True, verbose_name="专家组")

    def __str__(self):
        return self.username


