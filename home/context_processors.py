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