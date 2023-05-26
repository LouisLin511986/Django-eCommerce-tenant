from django.contrib import admin
from products.models import Product, ProductCategory, ProductImage # 匯入模型

class ProductImageInline(admin.TabularInline): # 內嵌管理介面
    model = ProductImage
    fields = ('name', 'image', 'order')

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category__name', 'product_Number'] # 設定列表頁面查詢框
    fields = ('product_Number', 'name', 'description', 'price', 'inventory', 'category', 'created', 'modified', 'date_Published')
    list_display = ('product_Number', 'name', 'price', 'inventory', 'category')
    list_filter = ('category',)
    autocomplete_fields = ['category'] # 新增修改頁面關聯欄位查詢框
    readonly_fields = ('product_Number', 'created', 'modified', 'date_Published')
    inlines = [ProductImageInline, ]

class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name'] # 設定列表頁面查詢框
    fields = ('name', 'description', 'created', 'modified', 'image')
    list_display = ('name', )
    readonly_fields = ('created', 'modified')

admin.site.register(Product, ProductAdmin)         # 註冊 Product 模型
admin.site.register(ProductCategory, ProductCategoryAdmin)    # 註冊 ProductCategory 模型