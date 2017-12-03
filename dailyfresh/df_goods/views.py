from django.shortcuts import render, redirect
from df_goods.models import Goods,GoodsImage
from df_goods.enums import *
from django.core.urlresolvers import reverse
from django_redis import get_redis_connection
from django.core.paginator import Paginator
# Create your views here.


# 页面上主要内容是显示每种水果的三个名称,和销量最好的四种商品
# 种类type_id,显示数量,排序方式sort

def index(request):
    # 调用自定义管理器类的函数查询数据库
    fruits_new = Goods.objects.get_goods_by_type(FRUIT,3,sort='new')
    fruits_hot = Goods.objects.get_goods_by_type(FRUIT,4,sort='hot')
    seafood_new = Goods.objects.get_goods_by_type(SEAFOOD, 3, sort='new')
    seafood_hot = Goods.objects.get_goods_by_type(SEAFOOD, 4, sort='hot')

    context = {'fruits_new':fruits_new, 'fruits_hot':fruits_hot,
               'seafood_new':seafood_new, 'seafood_hot':seafood_hot}
    return render(request, 'df_goods/index.html', context)


def detail(request, goods_id):
    # 获取商品信息，根据商品id查询数据库
    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    if goods is None:
        return redirect(reverse('goods:index'))
    # 获取图片,
    images = GoodsImage.objects.filter(goods_id=goods_id)

    if images.exists():
        image = images[0]
    else:
        image = ''
    # 查询新品推荐
    goods_li = Goods.objects.get_goods_by_type(type_id=goods.type_id, limit=2, sort='new')

    if request.session.has_key('is_login'):
        # 创建链接数据库的操作对象.记录浏览记录。
        con = get_redis_connection('default')
        key = 'history_%d'%request.session.get('passport_id')
        con.lrem(key, 0, goods.id)
        con.lpush(key, goods.id)
        # 截取五个
        con.ltrim(key, 0, 4)
    return render(request, 'df_goods/detail.html',{'goods':goods,
                                                   'goods_li':goods_li,
                                                   'image':image})


# /list/种类id/页码/?sort=的方式传递参数
def list(request, type_id, page):
    # 获取到查询方式，然后查询到商品
    sort = request.GET.get('sort', 'default')
    # 判断type_id是否合法
    if int(type_id) not in GOODS_TYPE.keys():
        return redirect(reverse('goods:index'))
    goods_li = Goods.objects.get_goods_by_type(type_id=int(type_id), sort=sort)
    # 对查询到的商品做分页显示
    paginator = Paginator(goods_li, 1)
    num_pages = paginator.num_pages
    print(num_pages)
    if page == '' or int(page) > num_pages:
        page = 1
    else:
        # 通过url匹配的参数都是字符串类型，转换成int类型
        page = int(page)
    # 获取第page页的数据
    goods_page = paginator.page(page)
    # 控制页码，每次显示5页
    """
    1，总页数小于5页时，直接显示1-5页
    2，总页数大于5时，当前点击页为前三页时，显示1-5页
    当前点击页为后3页时，显示后5页，当前点击页为前三页与后三页之间的，
    显示当前页的前两页和后两页
    """
    # 获取所有页码列表
    plist = paginator.page_range
    # 分页之后的总页码
    num_pages = paginator.num_pages
    if num_pages < 5:
        pages = range(1, 6)
    elif page <= 3:
        pages = range(1, 6)
    elif num_pages-page <= 2:
        pages = range(num_pages-4, num_pages+1)
    else:
        pages = range(page-2, page+3)
    # 获取新品推荐
    goods_new = Goods.objects.get_goods_by_type(type_id=type_id,limit=2,sort='new')
    type_title = GOODS_TYPE[int(type_id)]
    context = {'page':page,'goods_page':goods_page,
               'plist':plist,'goods_new':goods_new,"pages":pages,
               'type_id':type_id,'sort':sort,'type_title':type_title}
    return render(request,'df_goods/list.html',context)