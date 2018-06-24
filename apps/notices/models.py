from django.db import models
from datetime import datetime


# Create your models here.
class Notice(models.Model):
    name = models.CharField(max_length=100, verbose_name="公告名称")
    type = models.IntegerField(verbose_name="公告类型", choices=(
        (0, '创新创业项目公告'),
        (1, '立项公告'),
        (2, '结题公告')
    ), default=0)
    desc = models.TextField(verbose_name="公告描述", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="启动申报时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="截止申报时间", null=True, blank=True)
    deadline = models.DateTimeField(verbose_name="项目验收时间", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="公告发布时间")

    class Meta:
        verbose_name = "公告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class NoticeResource(models.Model):
    notice = models.ForeignKey(Notice, verbose_name="公告", on_delete=models.CASCADE)
    resource = models.FileField(upload_to='notices/%Y/%m', verbose_name="附件", null=True, blank=True)

    class Meta:
        verbose_name = "公告附件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.resource.name
