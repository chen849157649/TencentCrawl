from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash
# Create your models here.


class PassportManager(models.Manager):
    def add_one_passport(self, username, password, email):
        """ # self.model可获取类名Passport
        obj = self.model()  # 创建对象
        obj.username = username
        obj.password = password
        obj.email = email
        obj.save()"""
        # 可直接调用父类的create方法
        obj = self.create(username=username, password=get_hash(password), email=email)
        return obj

    def get_one_passport(self, username, password):
        try:
            passport = self.get(username=username, password=get_hash(password))
        except self.model.DoesNotExist:
            passport = None
        return passport


class Passport(BaseModel):
    username = models.CharField(verbose_name='账户', max_length=20)
    password = models.CharField(verbose_name='密码', max_length=40)
    email = models.EmailField(verbose_name='邮箱')
    is_active = models.BooleanField(verbose_name='激活状态', default=False)

    objects = PassportManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user_account'


class AddressManage(models.Manager):
    def get_default_address(self, passport_id):
        # 判断用户是否有默认地址
        try:
            address = self.get(passport_id=passport_id, is_default=True)

        except self.model.DoesNotExist:
            address = None

        return address

    def add_one_address(self,passport_id,recipient_name,recipient_addr,zip_code,recipient_phone):
        addr = self.get_default_address(passport_id)

        if addr:
            is_default = False

        else:
            # 若没有默认地址，则设置成默认
            is_default = True
        address = self.create(recipient_name=recipient_name,
                              recipient_addr=recipient_addr,
                              zip_code=zip_code,
                              recipient_phone=recipient_phone,
                              is_default=is_default,
                              passport_id=passport_id)
        return address


class Address(BaseModel):
    passport = models.ForeignKey('Passport')
    recipient_name = models.CharField(verbose_name='收件人',max_length=24)
    recipient_addr = models.CharField(verbose_name='收件地址', max_length=128)
    recipient_phone = models.CharField(verbose_name='电话', max_length=11)
    zip_code = models.CharField(verbose_name='邮编', max_length=6)
    is_default = models.BooleanField(verbose_name='是否默认', default=False)

    objects = AddressManage()

    class Meta:
        db_table = 'user_address'

    def __str__(self):
        return self.recipient_name



