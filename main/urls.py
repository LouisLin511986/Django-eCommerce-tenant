"""
這段程式碼代表了 Django 中 URL 配置的一部分。讓我來解釋它的含義：

```python
path('products/', include(('products.urls', 'products'), namespace='products'))
```

這個程式碼使用了 `path` 函數，該函數用於設置 URL 路由。下面是這個路由配置的詳細說明：

- `'products/'`：這是路徑模式，表示 URL 的開頭應該是 `products/`。
- `include(('products.urls', 'products'), namespace='products')`：這個部分是將路由指向 `products` 應用的 URL 配置。這裡使用了 `include` 函數，它將其他應用的 URL 配置文件包含進來。
  - `'products.urls'`：這是包含 `products` 應用的 URL 配置文件的路徑。這個文件將定義 `products` 應用的特定 URL 路由。
  - `'products'`：這是這個 URL 配置的名稱空間（namespace），用於區分不同應用之間的 URL。這個名稱空間可以讓我們在模板或代碼中引用特定應用的 URL。
  - `namespace='products'`：這是指定這個 URL 配置的名稱空間為 `'products'`。

簡而言之，這段程式碼的作用是將 URL 路由指向 `products` 應用的 URL 配置文件，並為這個 URL 配置指定了名稱空間 `'products'`。這樣可以在其他地方引用 `products` 應用的 URL 時使用這個名稱空間。
The example page :
    1.http://example01.localhost:8000/products/, 
    http://example01.localhost:8000/admin/
    2.http://example02.localhost:8000/products/
    http://example02.localhost:8000/admin/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('Dashboard/',  include ( 'admin_soft.urls' )), 
    path('i18n/', include('django.conf.urls.i18n')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('epaper/', include(('epaper.urls', 'epaper'), namespace='epaper')),
    path('customers/', include(('customers.urls', 'customers'), namespace='customers')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 新增 media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)