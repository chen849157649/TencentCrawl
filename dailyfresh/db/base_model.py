from django.db import models


class BaseModel(models.Model):
    is_delete = models.BooleanField(verbose_name='删除标记', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        abstract = True  # 说明这是一个抽象类，表示不产生此表

