from django.db.models import Max, Min
from .models import *
from django.core.cache import cache


def settings(request):
    context = dict()

    settings = cache.get('settings')
    if not settings:
        settings = Setting().getSettings()
        cache.set('settings', settings, 3600)

    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.order_by('id').select_related('image')
        cache.set('categories', categories, 3600)

    pages = cache.get('pages')
    if not pages:
        pages = Page.objects.filter(status=True).select_related('image')
        cache.set('pages', pages, 3600)

    price_range = cache.get('price_range')
    if not price_range:
        price_range = ObjectProperty.objects.aggregate(Max('price'), Min('price'))
        cache.set('price_range', price_range, 3600)

    context['categories'] = categories
    context['settings'] = settings
    context['base_url'] = settings.base_url
    context['pages'] = pages
    context['object_type'] = ObjectType.objects.all()
    context['locality'] = Locality.objects.all()
    context['rooms'] = Room.objects.all()
    context['storeys'] = Storey.objects.all()
    context['currency'] = Currency.objects.all()
    context['min_price'] = price_range['price__min']
    context['max_price'] = price_range['price__max']

    return context
