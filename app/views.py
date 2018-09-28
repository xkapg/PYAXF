import hashlib
import os
import uuid

from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
# def hello(request):
#     return HttpResponse('hello')
from AXF import settings
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User


# 首页
def home(request):
    # 轮播图
    wheels = Wheel.objects.all()
    # 导航
    navs = Nav.objects.all()
    # 每日必购
    mustbuys = Mustbuy.objects.all()
    # 商品部分
    shoplist = Shop.objects.all()
    shophead = shoplist[0]
    shoptab = shoplist[1:3]
    shopclass = shoplist[3:7]
    shopcommend = shoplist[7:11]
    # 商品主体
    mainshows = MainShow.objects.all()

    data = {
        'title': '首页',
        'wheels':wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead': shophead,
        'shoptab': shoptab,
        'shopclass': shopclass,
        'shopcommend': shopcommend,
        'mainshows': mainshows,
    }
    return render(request, 'home/home.html', context=data)

# 闪购超市
def market(request, categoryid, childid, sortid):
    # 分类数据
    foodtypes = Foodtypes.objects.all()

    # 获取点击 历史【typeIndex]
    # 无typeIndex, 默认为0
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    categoryid = foodtypes[typeIndex].typeid


    # 子类
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames  # 对应分类下 子类字符串
    childlist = []
    for item in childtypenames.split('#'):
        arr = item.split(':')
        obj = {'childname': arr[0], 'childid': arr[1]}
        childlist.append(obj)

    # 商品数据
    # goodslist = Goods.objects.all()[1:10]

    # 根据商品分类  过滤数据
    if childid == '0':  # 全部分类
        goodslist = Goods.objects.filter(categoryid=categoryid)
    else:   # 对应分类
        goodslist = Goods.objects.filter(categoryid=categoryid, childcid=childid)

    # 排序处理
    if sortid == '1':   # 销量排序
        goodslist= goodslist.order_by('productnum')
    elif sortid == '2': # 价格最低
        goodslist= goodslist.order_by('price')
    elif sortid == '3': # 价格最高
        goodslist= goodslist.order_by('-price')

    data = {
        'title': '闪购超市',
        'foodtypes':foodtypes,
        'goodslist':goodslist,
        'childlist':childlist,
        'categoryid':categoryid,
        'childid':childid
    }

    return render(request, 'market/market.html', context=data)

# 购物车
def cart(request):
    return render(request, 'cart/cart.html')

# 我的
def mine(request):
    token = request.session.get('token')

    responseData = {
        'title': '我的'
    }

    if token:   # 登录
        user = User.objects.get(token=token)
        responseData['name'] = user.name
        responseData['rank'] = user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['islogin'] = True
    else:       # 未登录
        responseData['name'] = '未登录'
        responseData['rank'] = '未登录'
        responseData['img'] = '/static/uploads/axf.png'
        responseData['islogin'] = False

    return render(request, 'mine/mine.html', context=responseData)

# 注册
def register(request):
    if request.method == 'POST':
        user = User()
        user.account = request.POST.get('account')
        user.password = generate_password(request.POST.get('password'))
        user.name = request.POST.get('name')
        user.tel = request.POST.get('tel')
        user.address = request.POST.get('address')

        # 头像
        imgName = user.account + '.png'
        imgPath = os.path.join(settings.MEDIA_ROOT, imgName)
        print(imgPath)
        file = request.FILES.get('file')
        print(file)
        with open(imgPath, 'wb') as fp:
            for data in file.chunks():
                fp.write(data)
        user.img = imgName

        # token
        user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))

        # 保存到数据库
        user.save()

        # 状态保持
        request.session['token'] = user.token

        # 重定向
        return redirect('axf:mine')

    elif request.method == 'GET':
        return render(request, 'mine/register.html')


# 密码
def generate_password(password):
    sha = hashlib.sha512()
    sha.update(password.encode('utf-8'))
    return sha.hexdigest()

# 退出登录
def quit(request):
    # request.session.flush()
    logout(request)
    return redirect('axf:mine')

# 登录
def login(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        try:
            user = User.objects.get(account=account)
            if user.password != generate_password(password):    # 密码错误
                return render(request, 'mine/login.html', context={'error': '密码错误!'})
            else:   # 登录成功
                # 更新token
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()
                # 状态保持
                request.session['token'] = user.token
                return redirect('axf:mine')
        except:
            return render(request, 'mine/login.html', context={'error':'用户名错误'})

    elif request.method == 'GET':
        return render(request, 'mine/login.html')


# 用户验证
def checkuser(request):
    account = request.GET.get('account')
    try:
        user = User.objects.get(account=account)
        return JsonResponse({'msg':'用户名存在', 'status':'-1'})
    except:
        return JsonResponse({'msg':'用户名可用', 'status':'1'})


# 添加购物车
def addtocart(request):
    return None