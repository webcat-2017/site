from django.http import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from .models import *
from django.core.cache import cache


def custom_page_not_found_view(request, exception):

    return render(request, "neruhomist/404.html", {})


def index(request):

    recommended = cache.get('recommended')
    if not recommended:
        recommended = ObjectProperty.objects.filter(recommended=True).select_related('image')
        cache.set('recommended', recommended, 3600)

    return render(request, 'neruhomist/index.html', {'recommended': recommended})


def category(request, category_id, page_num=1):

    category = Category.objects.get(id=category_id)

    objects = category.objectproperty_set.order_by('id')

    context = {'category': category}

    paginator = Paginator(objects, 6)

    try:
        context['objects'] = paginator.get_page(page_num)
    except PageNotAnInteger:
        context['objects'] = paginator.page(1)
    except EmptyPage:
        context['objects'] = paginator.page(paginator.num_pages)

    return render(request, 'neruhomist/objects.html', context)


def object(request, object_id):

    args = ['image', 'locality', 'category_object', 'street', 'area', 'rooms', 'storeys', 'currency']

    obj = ObjectProperty.objects.select_related(*args).get(id=object_id)

    context = dict()

    kwargs = {'object_type': obj.object_type, 'category_object': obj.category_object}

    context['interested'] = ObjectProperty.objects.exclude(pk=obj.id).select_related('image').filter(**kwargs)

    if obj.images.exists():

        context['images'] = obj.images.select_related('image').all()
        context['arrowsNav'] = 'true'

    else:
        context['arrowsNav'] = 'false'

    context['object'] = obj

    return render(request, 'neruhomist/object.html', context)


def page(request, page_id):

    p = Page.objects.get(id=page_id)
    context = dict()
    context['page'] = p
    return render(request, 'neruhomist/page.html', context)


def search(request, page_num=1):

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

        selected = request.read().decode('utf-8')

        if int(selected.split('=')[1]) == 4:
            response = JsonResponse({'fields': "block"})
        else:
            response = JsonResponse({'fields': "unblock"})
        return HttpResponse(response, content_type='application/json')

    if request.POST:
        query = QueryDict(request.readline())
        kwargs = dict()
        if int(query['category']):
            kwargs.update({'category_object_id': query['category']})

        if int(query['object_type']):
            kwargs.update({'object_type_id': query['object_type']})

        if int(query['locality']):
            kwargs.update({'locality_id': query['locality']})

        if int(query['storeys']):
            kwargs.update({'storeys_id': query['storeys']})

        if int(query['rooms']):
            kwargs.update({'rooms_id': query['rooms']})

        if int(query['currency']):
            kwargs.update({'currency_id': query['currency']})

        kwargs.update({'price__range': query['price'].split(';')})

        args = ['image', 'currency']

        objects = ObjectProperty.objects.filter(**kwargs).select_related(*args)

        context = dict()

        paginator = Paginator(objects, 6)

        try:
            context['objects'] = paginator.get_page(page_num)
        except PageNotAnInteger:
            context['objects'] = paginator.page(1)
        except EmptyPage:
            context['objects'] = paginator.page(paginator.num_pages)

        if objects:
            return render(request, 'neruhomist/objects.html', context)
        else:
            return render(request, 'neruhomist/object_not_found.html', context)
