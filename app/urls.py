from django.conf.urls import url

from app import views

urlpatterns = [
    # url(r'^hello/$', views.hello, name='hello'),
    # 主页
    url(r'^$', views.home, name='home'),
    # 闪购超市
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),
    # 购物车
    url(r'^cart/$', views.cart, name='cart'),
    # 我的
    url(r'^mine/$', views.mine, name='mine'),
    # 注册
    url(r'^register/$', views.register, name='register'),
    # 登录
    url(r'^login/$', views.login, name='login'),
    # 退出
    url(r'^logout/$', views.quit, name='logout'),
    # 用户名验证
    url(r'^checkuser/$', views.checkuser, name='checkuser'),
    # 添加购物车
    url(r'^addtocart/$', views.addtocart, name='addtocart'),

]