from .models import WebsiteSetting

def website_setting(request):
    if WebsiteSetting.objects.last():
        website_setting = WebsiteSetting.objects.last()
    else:
        website_setting = {}
    return {'website_setting': website_setting}