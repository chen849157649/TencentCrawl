from django.shortcuts import render
from django.http import JsonResponse
from df_goods.models import Goods
from django_redis import get_redis_connection
from utils.decorators import check_on
# Create your views here.


# 网页请求发过来的数据有商品数量和商品id，涉及到数据的修改用POST，一般获取数据请求才用GET，
def cart_add(request):
    # 先判断用户是否登录在线
    if not request.session.has_key('is_login'):
        return JsonResponse({'res':0, 'error_msg':'请先登录再添加商品'})
    # 获取数据
    goods_id = request.POST.get('goods_id')
    goods_count = request.POST.get('goods_count')
    # 验证数据的正确性
    if not all([goods_id, goods_count]):
        return JsonResponse({'res':1, 'error_msg':'参数不全'})
    try:
        count = int(goods_count)

    except Exception:
        return JsonResponse({'res':2, 'error_msg':'商品数量不合法'})
    # 查询商品信息
    goods= Goods.objects.get_goods_by_id(goods_id=goods_id)
    if not goods:
        return JsonResponse({'res':3, 'error_msg':'商品不存在'})
    # 向redis数据库添加用户准备购买的商品，采用hash数据类型保存
    con = get_redis_connection('default')
    key = 'cart_%d'%request.session.get('passport_id')
    # 添加商品数量时需要考虑用户的购物车之前是否有该商品
    res = con.hget(key, goods_id)  # 先获取用户某种商品的原有的数量
    if not res:
        # 用户之前购物车无商品
        res = count
    else:
        res = int(res) + count
    if count > goods.stock:
        return JsonResponse({'res': 4, 'error_msg':'库存不足'})
    else:
        con.hset(key, goods_id, res)
    return JsonResponse({'res':5})


# 当网页刷新就处理模板发送的GET请求获取商品总数量
def cart_count(request):
    if not request.session.has_key('is_login'):
        return JsonResponse({'res': 0})
    # 获取数据
    conn = get_redis_connection('default')
    key = 'cart_%d' % request.session.get('passport_id')
    # 若是计算商品的种类数，用redis的hlen方法即可
    # 若购物车显示商品总数，就需要将每个商品的数量相加，即获取某个键的所有属性值用hvals再相加
    res_list = conn.hvals(key)
    # 遍历取得每个商品的数量,再相加
    res = 0
    for i in res_list:
        res += int(i)
    return JsonResponse({'res':res})


@check_on
def cart_show(request):
    """展示购物车"""
    # 从redis数据库查询数据
    conn = get_redis_connection('default')
    key = 'cart_%d' % request.session.get('passport_id')
    res_dict = conn.hgetall(key)  # 返回值是一个字典
    total_price = 0
    total_count = 0
    goods_li = []
    # 遍历res_dict获取商品的信息
    for id,count in res_dict.items():
        # 模板中需要小计和数量，可以查询数据库得到商品对象，然后增加动态属性，
        # 然后模板中对象调用属性即可
        goods = Goods.objects.get_goods_by_id(goods_id=id)
        goods.count = count
        goods.amount = int(count)*goods.price
        goods_li.append(goods)
        # 计算总数和总价
        total_count += int(count)
        total_price += int(count)*goods.price
    context = {'goods_li':goods_li, 'total_count':total_count,
               'total_price':total_price}
    return render(request, 'df_cart/cart.html', context)


# 接收用户请求数据有goods_id,goods_count,
def cart_update(request):
    '''更新购物车商品数目'''
    # 判断用户是否登录
    if not request.session.has_key('is_login'):
        return JsonResponse({'res': 0, 'errmsg': '请先登录'})

    # 接收数据
    goods_id = request.POST.get('goods_id')
    goods_count = request.POST.get('goods_count')

    # 数据的校验
    if not all([goods_id, goods_count]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    if goods is None:
        return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

    try:
        goods_count = int(goods_count)
    except Exception as e:
        return JsonResponse({'res': 3, 'errmsg': '商品数目必须为数字'})
    # 更新操作
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % request.session.get('passport_id')

    # 判断商品库存
    if goods_count > goods.stock:
        return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
    # 更新redis数据的数据，即重新设置
    conn.hset(cart_key, goods_id, goods_count)

    return JsonResponse({'res': 5})


def cart_del(request):
    '''删除用户购物车中商品的信息'''
    # 判断用户是否登录
    if not request.session.has_key('is_login'):
        return JsonResponse({'res': 0, 'errmsg': '请先登录'})

    # 接收数据
    goods_id = request.POST.get('goods_id')

    # 校验商品是否存放
    if not all([goods_id]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    if goods is None:
        return JsonResponse({'res':2, 'errmsg':'商品不存存'})

    # 删除购物车商品信息
    conn = get_redis_connection('default')
    cart_key = 'cart_%d'%request.session.get('passport_id')
    conn.hdel(cart_key, goods_id)

    # 返回信息
    return JsonResponse({'res':3})









