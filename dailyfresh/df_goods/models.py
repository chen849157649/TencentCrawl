from django.db import models
from db.base_model import BaseModel
from df_goods.enums import *
from tinymce.models import HTMLField

# Create your models here.


class GoodsManager(models.Manager):
    def get_goods_by_type(self, type_id, limit=None, sort='default'):
        # order_by的参数是带引号的,filter,order_by等
        # 查询后返回的结果依然是查询集，可继续查，也可以如下形式使用
        if sort == 'new':
            args = ('-create_time',)
        elif sort == 'hot':
            args = ('-sales',)
        elif sort == 'price':
            args = ('price',)
        else:
            args = ('-pk',)
        # order_by()参数是不定长参数，可接收多个参数，*args可以当作可容纳多个变量组成的list或元组
        # 平时查询时直接传入一个参数，但是在调用函数使用时，变量的是不定长参数，若是接收到一个参数，
        # 就是order_by('-create_time'),若是两个参数，则就是order_by('-create_time','-sales')
        goods_li = self.filter(type_id=type_id).order_by(*args)
        if limit:
            goods_li = goods_li[:limit]
        return goods_li

    def get_goods_by_id(self, goods_id):
        try:
            goods = self.get(id=goods_id)
        except self.model.DoesNotExist:
            goods = None
        return goods
# 从enums中引入字典，生成字段类型choices的参数(一个2元元组的元组或者列表)
goods_type_choices = ((k, v) for k, v in GOODS_TYPE.items())
status_choices = ((k, v) for k, v in STATUS_CHOICE.items())


class Goods(BaseModel):
    type_id = models.SmallIntegerField(default=FRUIT, choices=goods_type_choices, verbose_name='商品种类')
    name = models.CharField(max_length=20, verbose_name='商品名称')
    desc = models.CharField(max_length=128, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    detail = HTMLField(verbose_name='商品详情')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    status = models.SmallIntegerField(default=ONLINE, choices=status_choices, verbose_name='商品状态')

    objects = GoodsManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 's_goods'


class ImageManger(models.Manager):
    '''商品图片模型管理器类'''
    pass


class GoodsImage(BaseModel):
    '''商品图片模型类'''
    goods = models.ForeignKey('Goods', verbose_name='所属商品')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')

    objects = ImageManger()

    class Meta:
        db_table = 's_goods_image'
