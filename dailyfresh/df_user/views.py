from django.shortcuts import render, redirect
from df_user.models import Passport,Address
from django.http import JsonResponse, HttpResponse
import re
from django.core.mail import send_mail
from django.conf import settings
from celery_tasks.tasks import send_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.core.urlresolvers import reverse
from utils.decorators import check_on
from django_redis import get_redis_connection
from df_goods.models import Goods
from df_order.models import OrderGoods,OrderInfo
# Create your views here.


def register(request):
    """显示注册页面"""
    return render(request, 'df_user/register.html')


def register_handle(request):
    """注册处理"""
    # 获取数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    # 进行数据校验,调用python的内置函数all()
    if not all([username, password, email]):
        # 若数据为空
        return render(request, 'df_user/register.html', {'errmsg': '参数不能为空!'})
    # 判断邮箱是否合法
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        # 邮箱不合法
        return render(request, 'df_user/register.html', {'errmsg': '邮箱不合法!'})

    # 注册
    passport = Passport.objects.add_one_passport(username, password, email)
    # 验证邮箱,send_mail是io阻塞，所以此处不采用，而使用异步神器celery
    # send_mail('天天生鲜邮箱验证','',settings.EMAIL_FROM,[email],html_message='<a href="http://www.baidu.com">百度</a>')
    # 生成token
    serializer = Serializer(settings.SECRET_KEY, 3600)
    token = serializer.dumps({'confirm':passport.id})
    token = token.decode()
    # 将任务发送到celery的broker那，
    send_active_email.delay(token, username, email)
    return redirect(reverse('goods:index'))


def user_active(request, token):
    """激活账号"""
    serializer = Serializer(settings.SECRET_KEY, 3600)
    try:
        info = serializer.loads(token)
        # 获取对象的id
        passport_id = info['confirm']
        # 查询激活用户是谁
        passport = Passport.objects.get(id=passport_id)
        # 激活用户
        passport.is_active = True
        passport.save()
        return redirect(reverse('user:login'))
    except Exception:
        return HttpResponse('链接已过期')


def check_user_exist(request):
    """注册过程中判断账号是否存在"""
    username = request.GET.get('user_name')
    list1 = Passport.objects.filter(username=username)
    if list1:
        return JsonResponse({'res': 0})  # 表示用户名已经注册
    else:
        return JsonResponse({'res': 1})


def login(request):
    """显示登录页面"""
    # 判断缓存中是否有用户名
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        checked = 'checked'
    else:
        username = ''
        checked = ''
    return render(request, 'df_user/login.html', {'username':username, 'checked':checked})


def login_check(request):
    """登录校验"""
    # 获取数据
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    # 验证数据
    if not all([username, password]):
        return JsonResponse({'res':2})
    # 查询是否存在
    passport = Passport.objects.get_one_passport(username=username, password=password)
    print(passport)
    if passport:
        # 从中间件设置中取出记录的路径，
        url_path = request.session.get('url_path',default=reverse('goods:index'))
        # 用户名正确时， 可以考虑记住用户名
        rsp = JsonResponse({'res': 1, 'url_path':url_path})
        if remember == 'true':
            rsp.set_cookie('username', username, max_age=3600*24*7)
        else:
            rsp.delete_cookie('username')
        # 用户能登录后，要保存登录状态和用户名，便于模板里使用
        request.session['is_login'] = True
        request.session['username'] = username  # session保存在服务器里
        request.session['passport_id'] = passport.id
        print(passport.id)
        return rsp  # 表示登录成功
    else:
        return JsonResponse({'res': 0})


def login_out(request):
    """退出登录"""
    # 退出后，跳转到首页
    request.session.flush()
    return redirect(reverse('goods:index'))


def user_online(request):

    return render(request, 'df_goods/index.html')


@check_on
def center_info(request):
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id)
    # 从redis数据库中获取用户的浏览记录,
    con = get_redis_connection('default')
    key = 'history_%d'%passport_id
    history_li = con.lrange(key, 0, 4)
    # 直接采用filter查询得到的结果集是按着默认id顺序的，redis中商品记录是按着最新浏览时间排序
    # 我们需按着浏览时间去展示商品，所以每次查询一个，添加到一个列表中，模板再遍历即可。
    goods_li = []
    for id in history_li:
        goods = Goods.objects.get_goods_by_id(goods_id=id)
        goods_li.append(goods)
    return render(request, 'df_user/user_center_info.html',{'addr':addr,'goods_li':goods_li})


@check_on
def center_order(request):
    passport_id = request.session.get('passport_id')
    # 查询订单表，获取订单信息,对应数据表查询很清楚思路的
    order_li = OrderInfo.objects.filter(passport_id=passport_id)
    for order in order_li:
        # 获取用户每个订单的order_id
        order_id = order.order_id
        order_goods_li = OrderGoods.objects.filter(order_id=order_id)
        for order_goods in order_goods_li:
            price = order_goods.price
            count = order_goods.count
            amount = int(count)*price
            order_goods.amount = amount
        order_li.order_goods_li = order_goods_li
    context = {'order_li':order_li}
    return render(request, 'df_user/user_center_order.html',context)


@check_on
def center_site(request):
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id)
    return render(request, 'df_user/user_center_site.html',{'addr':addr})


def address_handle(request):
    # 获取数据
    username = request.POST.get('receiver')
    address = request.POST.get('address')
    zip_code = request.POST.get('zip_code')
    telephone = request.POST.get('telephone')
    passport_id = request.session.get('passport_id')
    # 添加地址
    Address.objects.add_one_address(passport_id=passport_id,
                                    recipient_name=username,
                                    recipient_addr=address,
                                    zip_code=zip_code,
                                    recipient_phone=telephone)
    return redirect(reverse('user:center_site'))