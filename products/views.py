from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from products.models import *
from core.models import Setting
from .filters import ProductModelFilter
from products import models


class HomeView(TemplateView):
    template_name = "products/home.html"
        
    def get(self, request, *args, **kwargs): 
        products = Product.objects.all()
        # left_product_categories = ProductCategory.objects.all()[0:2]
        # right_product_categories = ProductCategory.objects.all()[2:3]
        # right_product_category = right_product_categories.first() if right_product_categories else None
        context = self.get_context_data(**kwargs)
        context['items'] = products
        # context['left_product_categories'] = left_product_categories
        # context['right_product_category'] = right_product_category
        return self.render_to_response(context)

"""
self: 表示视图函数的实例对象，用于访问类的成员变量和方法。
request: 表示 HTTP 请求对象，包含了客户端发送给服务器的请求信息，
    如请求头、请求体、请求方法、请求参数等。
*args: 表示可变长度的位置参数，可以接受任意数量的位置参数。
**kwargs: 表示可变长度的关键字参数，可以接受任意数量的关键字参数。
get 方法一般用于处理 HTTP GET 请求，并返回响应给客户端。request 
参数包含了客户端发送的请求信息，可以通过该参数访问请求的相关属性，
如请求方法、请求参数、请求头等。*args 和 **kwargs 参数用于接收视
图函数可能传递的额外参数，如路由中的参数或其他视图函数的参数。
"""

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'items'
    paginate_by = 10

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'item'

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response() is overridden.
        """
        setting = Setting.objects.first()
        template_name = 'products/detail/template1.html'
        
        if setting.detail_template == "Template-1":
            template_name = "products/detail/template1.html"
        elif setting.detail_template == "Template-2":
            template_name = "products/detail/template2.html"
        return [template_name]
    
def Productsearch(request):
    productall = models.Product.objects.all()  # 取得已啟用的產品, enabled=True
    productModelFilter = ProductModelFilter(queryset=productall)

    if request.method == "POST":
        productModelFilter = ProductModelFilter(request.POST, queryset=productall)
        context = {
		'productModelFilter': productModelFilter
		}
    return render(request, "products/search.html", locals())
