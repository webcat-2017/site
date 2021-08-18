from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
import requests
from xml import etree
import re
from django.conf import settings
from django import forms
from .models import *
from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from django.http import Http404, HttpResponseRedirect


admin.site.site_header = 'WEBCATcms'


class CategoryAdmin(admin.ModelAdmin):
    pass


def image_tag(obj):
    return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.image.url))


class ObjectPropertyImageAdmin(admin.ModelAdmin):
    pass


class ObjectPropertyImageInline(admin.StackedInline):
    model = ObjectPropertyImage
    max_num = 10
    extra = 0
    fields = ['image']


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['title', 'image', 'description', 'status', ]}),
        ('SEO налаштування', {'fields': ['meta_description']}),
        ('Розміщення', {'fields': [('menu', 'information', 'about_as')]}),
    ]


class ObjectTypeAdmin(admin.ModelAdmin):
    pass


class AreaAdmin(admin.ModelAdmin):
    pass


class CurrencyAdmin(admin.ModelAdmin):
    pass


"""
@receiver(post_save, sender=Area)
def my_handler(sender, instance, **kwargs):
    obj = ObjectProperty.objects.get(('area'))
    obj.area = instance.area
"""


class LocalityAdmin(admin.ModelAdmin):
    pass


class StreetAdmin(admin.ModelAdmin):
    pass


class RoomAdmin(admin.ModelAdmin):
    pass


class StoreyAdmin(admin.ModelAdmin):
    pass


class ObjectPropertyAdmin(admin.ModelAdmin):


    def post_to_channel(self, request, queryset):


        post = queryset.get()

        setting_site = Setting().getSettings()

        title = post.title

        image = setting_site.base_url + post.image.url

        description = ''

        description += description.join(etree.ElementTree.fromstring(post.description).itertext())

        keywords = ['Продаж', 'Продається', 'Оренда', 'Комерційна нерухомість', 'Квартира', 'Земельна ділянка', 'Будинок', 'Дачний масив']

        emojis = {'будинок': '🏠', 'квартира': '🏢', 'газ': '🔥', 'Газ': '🔥', 'вода': '🚰', 'Вода': '🚰', 'світло': '💡', 'Cвітло': '💡'}

        for keyword in keywords:
            if keyword in description:
                description = description.replace(keyword, '#' + keyword)
        for key, val in emojis.items():
            if key in description:
                description = description.replace(key, val + key)

        caption = ' 💥 ' + title + ' 💥 ' + '\n' + description + '\n' + 'Ціна  💵' + str(post.price) + ' ' + post.currency.sign

        params = {'chat_id': '@bla bla bla', 'photo': image, 'parse_mode': '', 'caption': caption,
                  'reply_markup': {
                      'InlineKeyboardMarkup': [[{
                                            "text": "Последние операции",
                                            "callback_data": "\/last"
                                                 },
                                                {
                                            "text": "Баланс",
                                            "callback_data": "\/balance"
                                                 }]]}}

        r = requests.get('https://api.telegram.org/bot3434343:dfgfdgfddf/sendPhoto', params=params)

    post_to_channel.short_description = "Вигрузити в соц. мережі"

    def image_tag(self, obj):
        return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.image.url))

    image_tag.short_description = 'Зображення'
    list_display = ('title', 'category_object', 'image_tag', 'object_type', 'published', 'status')

    inlines = [ObjectPropertyImageInline]

    fieldsets = [
        (None, {
            'fields': ['title', 'category_object', 'image', 'description', 'object_type', 'locality', 'area',
                       'street', 'price', 'currency', 'recommended', 'status', ]}),
        ('Додаткові характеристики', {'fields': ['cad_num', 'rooms', 'total_space', 'living_space', 'kitchen_space', 'height',
                                                 'floor', 'storeys']}),
        ('SEO налаштування', {'fields': ['meta_description']}),
    ]

    actions = ['post_to_channel']


class DontLog:
    def log_addition(self, *args):
        return ''


class SettingAdmin(DontLog, admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['title',
                     'base_url',
                     'work_schedule',
                     'phone_1',
                     'phone_2',
                     'phone_3',
                     'phone_4',
                     'email_1',
                     'email_2',
                     'link_facebook',
                     'link_instagram',
                     'link_telegram',
                     'site_image']}),
        ('SEO налаштування',
         {'fields': ['meta_description']}),
    ]

    def response_change(self, request, obj):
        return HttpResponseRedirect('/admin')

    def has_add_permission(self, request):
        """
            remove add and save and add another button
        """
        return False

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = True
        extra_context['show_delete'] = False
        extra_context['show_history'] = False
        return super(SettingAdmin, self).change_view(request, object_id, extra_context=extra_context)


admin.site.register(Page, PageAdmin)
admin.site.register(ObjectType, ObjectTypeAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Storey, StoreyAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ObjectProperty, ObjectPropertyAdmin)
admin.site.register(ObjectPropertyImage, ObjectPropertyImageAdmin)
admin.site.register(Setting, SettingAdmin)



