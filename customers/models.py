import os
from django.conf import settings
from django.db import models, connection
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    schema_name = models.CharField(verbose_name="架構名稱")
    name = models.CharField(verbose_name = "租戶名稱", max_length=100) #租戶名稱
    paid_until =  models.DateTimeField(verbose_name = "截止日期") #截止日期
    on_trial = models.BooleanField (verbose_name = "正在試用") #正在試用
    created_on = models.DateTimeField(verbose_name = "加入日期", auto_now = True) 

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    auto_drop_schema = True

    class Meta:
        verbose_name = ('租戶')
        verbose_name_plural = ('租戶')
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.name}'

    def delete(self, force_drop=False, *args, **kwargs):
        """
        Deletes this row. Drops the tenant's schema if the attribute
        auto_drop_schema set to True.
        """
        locale_path = locale_path = os.path.join(settings.BASE_DIR, f'tenant_locale/{connection.schema_name}')
        os.system(f"rm -rf {locale_path}")
        self._drop_schema(force_drop)
        super().delete(*args, **kwargs)

class Domain(DomainMixin):
    domain = models.CharField(verbose_name="網域")
    is_primary = models.BooleanField(verbose_name="主要網域")

    class Meta:
        verbose_name = ('網域')
        verbose_name_plural = ('網域')

    def __str__(self):
        return f'{self.domain}'