from .models import Community

def communities_processor(request):
    communities = Community.objects.all()

    return {'communities': communities}
