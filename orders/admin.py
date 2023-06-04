from django.contrib import admin
from orders.models import Order
from products.models import RelationalProduct

class RelationalProductInline(admin.TabularInline):
    model = RelationalProduct
    verbose_name = '商品名稱'
    extra = 2
    fields = ('name', 'price', 'number')
    readonly_fields = ('name', 'price', 'number')

    # 这个方法用于控制是否允许添加新的关联产品，这里返回False，表示不允许添加。
    def has_add_permission(self, request, obj):
        return False

    # 这个方法用于控制是否允许删除关联的产品，这里返回False，表示不允许删除。
    def has_delete_permission(self, request, obj=None):
        return False

    def name(self, instance):
        return instance.product.name

    def price(self, instance):
        return instance.product.price

    name.short_description = '商品名稱'  # 设置字段的显示名称
    price.short_description = '商品價格'  # 设置字段的显示名称

class OrderAdmin(admin.ModelAdmin):
    model = Order
    search_fields = ['order_id', 'name']
    fields = ('order_id', 'name', 'email', 'phone', 'district', 'zipcode', 'address', 'total', 'status', 'created', 'modified')
    list_display = ('order_id', 'name', 'email', 'total', 'status')
    list_filter = ('status',)
    readonly_fields = ('order_id', 'name', 'email', 'phone', 'district', 'zipcode', 'address', 'total', 'created', 'modified')
    inlines = [RelationalProductInline,]

admin.site.register(Order, OrderAdmin)