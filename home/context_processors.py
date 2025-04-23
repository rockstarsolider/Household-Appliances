def website_setting(request):
    try:
        from .models import WebsiteSetting
        if WebsiteSetting.objects.last():
            website_setting = WebsiteSetting.objects.last()
        else:
            website_setting = {}
        return {'website_setting': website_setting}
    except:
        return {'website_setting': {}}
    
def categories(request):
    try:
        from products.models import Category
        if Category.objects.last():
            context_categories = Category.objects.all()[:15]
        else:
            context_categories = {}
        return {'context_categories': context_categories}
    except:
        return {'context_categories': {}}