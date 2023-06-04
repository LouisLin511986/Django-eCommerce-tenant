import base64
import pickle
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from .forms import *
from products.models import *
from datetime import datetime
from .ecpay_payment_sdk import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
                if product := Product.objects.filter(product_Number=product_id):
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
    
class ClearCartView(View):
    def get(self, request, *args, **kwargs):
        response = JsonResponse({"status": 200})
        response.delete_cookie("cart")
        return response
        
class CheckoutView(FormView):
    template_name = "orders/checkout.html"   # 結帳頁面

    form_class = OrderForm
    success_url = 'orders/confirmation.html' # 前往付款頁面

    def get_cart_cookie(self, request):
        cart_str = request.COOKIES.get('cart', '')
        product_dict = {}
        if cart_str:
            cart_bytes = cart_str.encode()
            cart_bytes = base64.b64decode(cart_bytes)
            cart_dict = pickle.loads(cart_bytes)
        return cart_dict
    
    def get(self, request, *args, **kwargs):
        cart_dict = self.get_cart_cookie(request)
        product_dict = {}
        total = 0
        if cart_dict:
            for product_id in cart_dict:
                if product := Product.objects.filter(product_Number=product_id):
                    product_dict[product_id] = {
                        "product": product.first(),
                        "count": cart_dict[product_id]["count"]
                    }
                    total += int(cart_dict[product_id]["count"]) * int(product.first().price)
        context = self.get_context_data(**kwargs)
        context["product_dict"] = product_dict
        context["total"] = total
        return self.render_to_response(context)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        cart_dict = self.get_cart_cookie(self.request)
        total = 0
        if cart_dict:
            for product_id in cart_dict:
                if product := Product.objects.filter(product_Number=product_id):
                    # 先保存 self.object
                    self.object.save()
                    # 創建 RelationalProduct
                    RelationalProduct.objects.create(order=self.object, product=product.first(), number=cart_dict[product_id]["count"])
                    total += int(cart_dict[product_id]["count"]) * int(product.first().price)
        self.object.total = total
        self.object.status = "未付款"
        self.object.save()
        context = self.get_context_data(form=form)
        context['order_id'] = self.object.order_id
        return render(self.request, self.success_url, context=context)

#對應 綠界科技金流表單視圖【https://developers.ecpay.com.tw/?p=2856】
class ECPayView(TemplateView):
    template_name = "orders/ecpay.html"

    def post(self, request, *args, **kwargs):
        scheme = request.is_secure() and "https" or "http"
        domain = request.META['HTTP_HOST']

        order_id = request.POST.get("order_id")
        order = Order.objects.get(order_id=order_id)
        product_list = "#".join([product.name for product in order.product.all()])
        order_params = {
            'MerchantTradeNo': order.order_id,
            'StoreID': '',
            'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            'PaymentType': 'aio',
            'TotalAmount': order.total,
            'TradeDesc': order.order_id,
            'ItemName': product_list,
            'ReturnURL': f'{scheme}://{domain}/orders/return/', # ReturnURL為付款結果通知回傳網址，為特店server或主機的URL，用來接收綠界後端回傳的付款結果通知。
            'ChoosePayment': 'ALL',
            'ClientBackURL': f'{scheme}://{domain}/products/list/', # 消費者點選此按鈕後，會將頁面導回到此設定的網址(返回商店按鈕)
            'ItemURL': f'{scheme}://{domain}/products/list/', # 商品銷售網址
            'Remark': '交易備註',
            'ChooseSubPayment': '',
            'OrderResultURL': f'{scheme}://{domain}/orders/orderresult/', # 消費者付款完成後，綠界會將付款結果參數以POST方式回傳到到該網址
            'NeedExtraPaidInfo': 'Y',
            'DeviceSource': '',
            'IgnorePayment': '',
            'PlatformID': '',
            'InvoiceMark': 'N',
            'CustomField1': '',
            'CustomField2': '',
            'CustomField3': '',
            'CustomField4': '',
            'EncryptType': 1,
        }
        # 建立實體，特店測試資料： 模擬銀行3D驗證
        ecpay_payment_sdk = ECPayPaymentSdk(
            MerchantID='3002607',
            HashKey='pwFHCqoQZGmho4w6',
            HashIV='EkRm7iFT261dpevs'
        )
        # 建立實體，平台商測試資料
        # ecpay_payment_sdk = ECPayPaymentSdk(
        #     MerchantID='3002599',
        #     HashKey='spPjZn66i0OhqJsQ',
        #     HashIV='hT5OJckN45isQTTs'
        # )
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        ecpay_form = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        context = self.get_context_data(**kwargs)
        context['ecpay_form'] = ecpay_form
        return self.render_to_response(context)
    
#對應 綠界科技金流伺服器端回應視圖
class ReturnView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ReturnView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # 建立實體，特店測試資料： 模擬銀行3D驗證
        ecpay_payment_sdk = ECPayPaymentSdk(
            MerchantID='3002607',
            HashKey='pwFHCqoQZGmho4w6',
            HashIV='EkRm7iFT261dpevs'
        )
        # 建立實體，平台商測試資料
        # ecpay_payment_sdk = ECPayPaymentSdk(
        #     MerchantID='3002599',
        #     HashKey='spPjZn66i0OhqJsQ',
        #     HashIV='hT5OJckN45isQTTs'
        # )
        res = request.POST.dict()
        back_check_mac_value = request.POST.get('CheckMacValue')
        check_mac_value = ecpay_payment_sdk.generate_check_value(res)
        if check_mac_value == back_check_mac_value:
            self.clear_cart()
            return HttpResponse('1|OK')
        return HttpResponse('0|Fail')
        
#對應 綠界科技金流用戶端端回應視圖
class OrderResultView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderResultView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # 建立實體，特店測試資料： 模擬銀行3D驗證
        ecpay_payment_sdk = ECPayPaymentSdk(
            MerchantID='3002607',
            HashKey='pwFHCqoQZGmho4w6',
            HashIV='EkRm7iFT261dpevs'
        )
        # 建立實體，平台商測試資料
        # ecpay_payment_sdk = ECPayPaymentSdk(
        #     MerchantID='3002599',
        #     HashKey='spPjZn66i0OhqJsQ',
        #     HashIV='hT5OJckN45isQTTs'
        # )
        res = request.POST.dict()
        back_check_mac_value = request.POST.get('CheckMacValue')
        order_id = request.POST.get('MerchantTradeNo')
        rtnmsg = request.POST.get('RtnMsg')
        rtncode = request.POST.get('RtnCode')
        check_mac_value = ecpay_payment_sdk.generate_check_value(res)
        if check_mac_value == back_check_mac_value and rtnmsg == 'Succeeded' and rtncode == '1':
            order = Order.objects.get(order_id=order_id)
            order.status = '已付款，等待裝運'
            order.save()
            return HttpResponseRedirect('/orders/order_success/')
        else:
            order = Order.objects.get(order_id=order_id)
            order.status = '付款失敗'
            order.save()
            return HttpResponseRedirect('/orders/order_fail/')
        
    
    
#對應 付款成功視圖
class OrderSuccessView(TemplateView):
    template_name = "orders/order_success.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
#對應 付款失敗視圖
class OrderFailView(TemplateView):
    template_name = "orders/order_fail.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)