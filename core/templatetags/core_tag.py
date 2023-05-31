from django import template
register = template.Library()
from core.models import Setting

@register.simple_tag
def get_setting():
    setting = Setting.objects.first()  # 获取第一个设置对象
    setting_dict = {}

    if setting:
        setting_dict['favicon'] = setting.favicon
        setting_dict['sitename'] = setting.sitename
        setting_dict['logo'] = setting.logo
        setting_dict['style'] = setting.style
        setting_dict['detail_template'] = setting.detail_template
        setting_dict['facebook'] = setting.facebook
        setting_dict['instagram'] = setting.instagram
        setting_dict['twitter'] = setting.twitter
        if setting.home_type1:
            setting_dict['home_type1'] = {
                'name': setting.home_type1.name,
                'image': setting.home_type1.image,
                'description': setting.home_type1.description
            }
        if setting.home_type2:
            setting_dict['home_type2'] = {
                'name': setting.home_type2.name,
                'image': setting.home_type2.image,
                'description': setting.home_type2.description
            }
        if setting.home_type3:
            setting_dict['home_type3'] = {
                'name': setting.home_type3.name,
                'image': setting.home_type3.image,
                'description': setting.home_type3.description
            }

    return setting_dict

# @register.simple_tag
# def get_setting_list():
#     settings = Setting.objects.all()
#     return [{"code": setting.id, "name_local": setting.language} for setting in settings]