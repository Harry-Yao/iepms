from django.db import models

from datetime import datetime

from notices.models import Notice
from users.models import UserProfile, ExpertGroup


# 学生课题
class Project(models.Model):
    p_name = models.CharField(max_length=100, verbose_name="课题名称")
    p_notice = models.ForeignKey(Notice, verbose_name="所属项目")
    p_type = models.IntegerField(verbose_name="课题类型", choices=(
        (0, "创新训练"),
        (1, "创业训练"),
        (2, "创业实践")
    ))
    p_leader = models.ForeignKey(UserProfile, verbose_name="项目负责人")
    p_application = models.FileField(upload_to="application/%Y/%m", verbose_name="项目申请书")
    p_middle = models.FileField(upload_to="middle/%Y/%m", verbose_name="中期报告", null=True, blank=True)
    p_status = models.IntegerField(verbose_name="项目状态", choices=(
        (0, "待审核"),
        (1, "待评分"),
        (2, "待立项"),
        (3, "已立项"),
        (4, "中期检查"),
        (5, "中期检查通过"),
        (6, "已验收"),
        (7, "驳回重填"),
        (8, "延期审核中"),
        (9, "已延期"),
        (10, "终止"),
        (11, "中期审核中"),
    ), default=0)
    p_desc = models.TextField(verbose_name="项目简介", null=True, blank=True)
    p_comment = models.TextField(verbose_name="初审意见", null=True, blank=True)
    p_level = models.IntegerField(verbose_name="立项级别", choices=(
        (0, "未立项"),
        (1, "校级立项"),
        (2, "省级立项"),
        (3, "国家级立项")
    ), default=0)
    p_code = models.IntegerField(verbose_name="项目所属一级学科代码", null=True, blank=True)
    financial_appropriation = models.IntegerField(verbose_name="财政拨款（元）",  null=True, blank=True)
    college_appropriation = models.IntegerField(verbose_name="学校拨款（元）",  null=True, blank=True)
    d_name = models.CharField(max_length=20, verbose_name="负责人姓名")
    d_gender = models.CharField(max_length=7, verbose_name="负责人性别", choices=(
        ("male", "男"),
        ("female", "女")
    ), default="male")
    d_phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="负责人联系电话")
    d_qq = models.CharField(max_length=20, null=True, blank=True,  verbose_name="负责人QQ")
    d_major = models.CharField(max_length=10, verbose_name="负责人专业")
    d_student_id = models.CharField(max_length=20, verbose_name="负责人学号")
    d_college = models.IntegerField(verbose_name="所属学院", choices=(
        (0, '电子信息学院'),
        (1, '机电工程学院'),
        (2, '计算机学院'),
        (3, '材料与食品学院'),
        (4, '人文社会科学学院'),
        (5, '管理学院'),
        (6, '经贸学院'),
        (7, '外国语学院'),
        (8, '艺术设计学院')
    ), default=0)  # college
    d_email = models.EmailField(max_length=50, verbose_name="负责人邮箱")

    t_name = models.CharField(max_length=10, verbose_name="指导老师")
    t_gender = models.CharField(max_length=7, verbose_name="指导老师性别", choices=(
        ("male", "男"),
        ("female", "女")
    ))
    t_nation = models.CharField(max_length=10, null=True, blank=True, verbose_name="指导老师民族")
    t_birthday = models.DateField(verbose_name="指导老师生日", null=True, blank=True)
    t_title = models.CharField(max_length=10, null=True, blank=True, verbose_name="专业/职称/职务")
    t_phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="指导老师联系电话")
    t_email = models.EmailField(max_length=50, null=True, blank=True, verbose_name="指导老师邮箱")

    expert_group = models.ForeignKey(ExpertGroup, verbose_name="项目所属专家组", null=True, blank=True)
    deadline = models.DateTimeField(verbose_name="最后期限", null=True, blank=True)
    delay_result = models.TextField(verbose_name="延期原因",  null=True, blank=True)
    e_comment = models.TextField(verbose_name="专家意见", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "学生课题"
        verbose_name_plural = verbose_name

        ordering = ['p_status']

    def get_score(self):
        gande = 0
        scores = Score.objects.filter(project=self)
        if scores.count() != 0:
            for score in scores:
                gande += score.score
            return gande / scores.count()
        return gande
    get_score.short_description = "平均分"

    def get_member(self):
        members = ""
        if self.member_set.count() != 0:
            for member in self.member_set.all():
                tmp = member.m_name + "/" + member.m_student_id + " "
                members += tmp
            return members
        else:
            return "无"
        # return self.member_set.all()
    get_member.short_description = "项目成员"

    def member_num(self):
        return self.member_set.count() + 1
    member_num.short_description = "参与人数"

    def __str__(self):
        return self.p_name


class Member(models.Model):
    project = models.ForeignKey(Project, verbose_name="所属项目", on_delete=models.CASCADE)
    m_name = models.CharField(max_length=10, verbose_name="姓名")
    m_sex = models.CharField(max_length=7, verbose_name="性别", choices=(
        ("male", "男"),
        ("female", "女")
    ))
    m_phone = models.CharField(max_length=11, verbose_name="联系电话")
    m_major = models.CharField(max_length=10, verbose_name="专业")
    m_grade = models.CharField(max_length=10, verbose_name="年级")
    m_student_id = models.CharField(max_length=20, verbose_name="学号")
    m_college = models.IntegerField(verbose_name="所属学院", choices=(
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

    class Meta:
        verbose_name = "项目成员"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.m_name


class Score(models.Model):
    expert = models.ForeignKey(UserProfile, verbose_name="专家")
    project = models.ForeignKey(Project, verbose_name="学生课题")
    score = models.IntegerField(verbose_name="分数")

    class Meta:
        verbose_name = "评分"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.score


