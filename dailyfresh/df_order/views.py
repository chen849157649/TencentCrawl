from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from df_user.models import Address
from django_redis import get_redis_connection
from df_goods.models import Goods
from df_order.models import OrderGoods,OrderInfo
from datetime import datetime
# Create your views here.


# 在前端被选中的checkbox标签有多个，所以POST中的goods_ids对应多个商品id
def order_place(request):
    # 获取数据
    goods_ids = request.POST.getlist('goods_ids')
    if not all([goods_ids]):
        # 跳转会购物车页面
        return redirect(reverse('cart:show'))
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)
    # 连接上redis数据库，获取商品id和数量
    con = get_redis_connection('default')
    cart_key = 'cart_%d'%passport_id
    goods_li = []
    total_count = 0
    total_price = 0
    for id in goods_ids:
        goods = Goods.objects.get_goods_by_id(goods_id=id)
        count = con.hget(cart_key, id)
        amount = goods.price*int(count)  # 商品小计
        goods.amount = amount
        goods.count = count
        goods_li.append(goods)

        total_count += int(count)
        total_price += amount

    transmit_price = 10
    total_pay = total_price + transmit_price

    goods_ids = ','.join(goods_ids)
    context = {'goods_li':goods_li, 'total_count':total_count,
               'total_price':total_price, 'transmit_price':transmit_price,
               'total_pay':total_pay, 'goods_ids':goods_ids,
               'addr':addr}
    return render(request, 'df_order/place_order.html', context)


# 接收参数,收货地址,支付方式,商品id
def order_commit(request):
    # 验证用户是否登录
    if not request.session.has_key('is_login'):
        return JsonResponse({'res': 0, 'errmsg': '用户未登录'})
    # 接收数据
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    goods_ids = request.POST.get('goods_ids')
    # 进行数据校验
    if not all([addr_id, pay_method, goods_ids]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

    try:
        addr = Address.objects.get(id=addr_id)  # 查询地址
    except Exception:
        # 地址信息出错
        return JsonResponse({'res': 2, 'errmsg': '地址信息错误'})
    if int(pay_method) not in OrderInfo.PAY_METHODS_ENUM.values():
        return JsonResponse({'res': 3, 'errmsg': '不支持的支付方式'})
    # 1.向订单表中添加一条信息
    # 2.遍历向订单商品表中添加信息
        # 2.1 添加订单商品信息之后，增加商品销量，减少库存
        # 2.2 累计计算订单商品的总数目和总金额
    # 3.更新订单商品的总数目和总金额
    # 4.清除购物车对应信息
    passport_id = request.session.get('passport_id')
    # 订单id: 20171029110830+用户的id
    order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(passport_id)
    #
    transit_price = 10
    total_count = 0
    total_price = 0
    # 向数据库中添加了一条购物记录,记录了某个用户的购买商品数量，总价，支付方式等
    order = OrderInfo.objects.create(order_id=order_id,total_count=total_count,
                                    total_price=total_price, transit_price=transit_price,
                                   pay_method=pay_method,
                                   addr_id=addr_id, passport_id=passport_id)
    # 向订单商品详情表添加数据
    print(order)
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % passport_id
    goods_ids = goods_ids.split(',')  # 传过来的是字符串
    for id in goods_ids:
        goods = Goods.objects.get_goods_by_id(goods_id=id)
        if goods is None:
            return JsonResponse({'res': 4, 'errmsg': '商品信息错误'})

        count = conn.hget(cart_key, id)  # 购物车的商品数量
        # 判断商品的库存
        if int(count) > goods.stock:
            return JsonResponse({'res': 5, 'errmsg': '商品库存不足'})
        OrderGoods.objects.create(count=count,price=goods.price,
                                  order_id=order_id, goods_id=id)
        # 增加销量，减少库存

        goods.sales += int(count)
        goods.stock -= int(count)
        goods.save()
        print(goods.sales)
        total_count += int(count)
        total_price += int(count)*goods.price

    # 之前添加时 默认0，现在更新数据
    order.total_price = total_price
    order.total_count = total_price
    order.save()
    # 删除购物车记录
    conn.hdel(cart_key, *goods_ids)
    return JsonResponse({'res':6})