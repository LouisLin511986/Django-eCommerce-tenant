import base64
import pickle
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View, TemplateView
from products.models import Product


class CartView(TemplateView):
    template_name = "orders/cart.html"

    def get(self, request, *args, **kwargs):
        cart_str = request.COOKIES.get('cart', '')
        product_dict = {}
        if cart_str:
            cart_bytes = cart_str.encode()
            cart_bytes = base64.b64decode(cart_bytes)
            cart_dict = pickle.loads(cart_bytes)
            product_dict = cart_dict.copy()
            for product_id in cart_dict:
                if product := Product.objects.filter(id=product_id):
                    product_dict[product_id]["product"] = product.first()
                else:
                    del product_dict[product_id]
        context = self.get_context_data(**kwargs)
        context["product_dict"] = product_dict
        return self.render_to_response(context)

class AddCartView(View):

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id', '')
        cart_str = request.COOKIES.get('cart', '')
        if product_id:
            if cart_str:
                cart_bytes = cart_str.encode()
                cart_bytes = base64.b64decode(cart_bytes)
                cart_dict = pickle.loads(cart_bytes)
            else:
                cart_dict = {}
            if product_id in cart_dict:
                cart_dict[product_id]['count'] += 1
            else:
                cart_dict[product_id] = {
                    'count': 1,
                }
            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
        context = {}
        context["status"] = 200
        response = JsonResponse(context)
        response.set_cookie("cart", cart_str)
        return response
    
class DeleteCartView(View):

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id', '')
        cart_str = request.COOKIES.get('cart', '')
        if product_id:
            if cart_str:
                cart_bytes = cart_str.encode()
                cart_bytes = base64.b64decode(cart_bytes)
                cart_dict = pickle.loads(cart_bytes)
            else:
                cart_dict = {}
            if product_id in cart_dict:
                del cart_dict[product_id]
            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
        context = {}
        context["status"] = 200
        response = JsonResponse(context)
        response.set_cookie("cart", cart_str)
        return response
    
# class CheckoutView(FormView):
#     template_name = "orders/checkout.html"   # 結帳頁面

#     form_class = OrderForm
#     success_url = 'orders/confirmation.html' # 前往付款頁面

#     def get_cart_cookie(self, request):
#         cart_str = request.COOKIES.get('cart', '')
#         product_dict = {}
#         if cart_str:
#             cart_bytes = cart_str.encode()
#             cart_bytes = base64.b64decode(cart_bytes)
#             cart_dict = pickle.loads(cart_bytes)
#         return cart_dict
    
#     def get(self, request, *args, **kwargs):
#         cart_dict = self.get_cart_cookie(request)
#         if cart_dict:
#             product_dict = cart_dict.copy()
#             total = 0
#             for product_id in cart_dict:
#                 if product := Product.objects.filter(id=product_id):
#                     product_dict[product_id]["product"] = product.first()
#                     total += int(product_dict[product_id]["count"]) * int(product.first().price)
#                 else:
#                     del product_dict[product_id]
#         context = self.get_context_data(**kwargs)
#         context["product_dict"] = product_dict
#         context["total"] = total
#         return self.render_to_response(context)
    
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         cart_dict = self.get_cart_cookie(self.request)
#         self.object.save()
#         if cart_dict:
#             total = 0
#             for product_id in cart_dict:
#                 if product := Product.objects.filter(id=product_id):
#                     RelationalProduct.objects.create(order=self.object, product=product.first(), number=cart_dict[product_id]["count"])
#                     total += int(cart_dict[product_id]["count"]) * int(product.first().price)
#         self.object.total = total
#         self.object.save()
#         context = self.get_context_data(form=form)
#         context['order_id'] = self.object.order_id
#         return render(self.request, self.success_url, context=context)