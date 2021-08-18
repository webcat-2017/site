from django.db import models
from django.core import validators
from django.conf import settings
from model_utils import Choices
from filer.fields.image import FilerImageField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Setting(models.Model):
    title = models.CharField(
        "Заголовок",
        max_length=30)

    base_url = models.URLField(
        "Головне посилання",
        max_length=50,
        validators=[validators.URLValidator(schemes=['http', 'https'])],)

    meta_description = models.TextField(
        "Мета опис",
        max_length=100,
        null=True,
        blank=True)

    work_schedule = models.CharField(
        "Графік роботи",
        max_length=30,
        null=True,
        blank=True)

    phone_1 = models.CharField(
        "Телефон №1",
        max_length=30,
        null=True,
        blank=True,
        validators=[validators.RegexValidator(regex='^[0-9]{10}$')],
        error_messages={'invalid': 'некоректний формат телефону'})

    phone_2 = models.CharField(
        "Телефон №2",
        max_length=30,
        null=True,
        blank=True,
        validators=[validators.RegexValidator(regex='^[0-9]{10}$')],
        error_messages={'invalid': 'некоректний формат телефону'})

    phone_3 = models.CharField(
        "Телефон №3",
        max_length=30,
        null=True,
        blank=True,
        validators=[validators.RegexValidator(regex='^[0-9]{10}$')],
        error_messages={'invalid': 'некоректний формат телефону'})

    phone_4 = models.CharField(
        "Телефон №4",
        max_length=30,
        null=True,
        blank=True,
        validators=[validators.RegexValidator(regex='^[0-9]{10}$')],
        error_messages={'invalid': 'некоректний формат телефону'})

    email_1 = models.CharField(
        "Почта №1",
        max_length=30,
        null=True,
        blank=True,
        validators=[validators.validate_email],
        error_messages={'invalid': 'некоректний формат скриньки'})

    email_2 = models.CharField(
        "Почта №2",
        max_length=30,
        null=True,
        blank=True,
        validators=[validators.validate_email],
        error_messages={'invalid': 'некоректний формат скриньки'})

    link_facebook = models.CharField(
        "Посилання Facebook",
        max_length=100,
        null=True,
        blank=True)

    link_instagram = models.CharField(
        "Посилання Instagram",
        max_length=100,
        null=True,
        blank=True)

    link_telegram = models.CharField(
        "Посилання Telegram",
        max_length=50,
        null=True,
        blank=True)

    site_image = FilerImageField(
        null=True,
        blank=True,
        related_name="site_image",
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Налаштування"
        verbose_name_plural = "Налаштування"

    def getSettings(self):

        settings = Setting.objects.get(id=1)

        def phone_split(x):
            if x[0:3] in ["039", "067", "068", "096", "097", "098"]:
                logo = "kyivstar.png"
            elif x[0:3] in ["050", "066", "095", "099"]:
                logo = "vodafone.png"
            elif x[0:3] in ["063", "073", "093"]:
                logo = "lifecell.png"
            else:
                logo = ''
            return {'phone': '-'.join([x[0:3], x[3:6], x[6:8], x[8:]]), 'logo': logo}

        settings.phone_1 = phone_split(settings.phone_1)
        settings.phone_2 = phone_split(settings.phone_2)
        settings.phone_3 = phone_split(settings.phone_3)
        settings.phone_4 = phone_split(settings.phone_4)

        return settings


class Locality(models.Model):

    name = models.CharField(
        "Назва",
        max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Населенный пункт"
        verbose_name_plural = "Населенні пункти:"


class Area(models.Model):

    name = models.CharField(
        "Назва",
        max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Район/Массив"
        verbose_name_plural = "Райони/Массиви"


class Street(models.Model):

    name = models.CharField(
        "Назва",
        max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вулиця"
        verbose_name_plural = "Вулиці"


class Room(models.Model):

    name = models.CharField(
        "Назва",
        max_length=30,
        blank=True,
        null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кількість кімнат"
        verbose_name_plural = "Кількість кімнат"


class Storey(models.Model):

    name = models.CharField(
        "Назва",
        max_length=30,
        blank=True,
        null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поверховість"
        verbose_name_plural = "Поверховість"


class Currency(models.Model):

    name = models.CharField(
        "Назва",
        max_length=30)

    sign = models.CharField(
        "Знак",
        blank=True,
        null=True,
        max_length=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюти"


class Category(models.Model):
    title = models.CharField(
        "Назва",
        max_length=30)

    description = RichTextUploadingField("Опис")
    image = FilerImageField(
        null=True,
        blank=True,
        related_name="image",
        on_delete=models.SET_NULL)

    meta_description = models.TextField(
        "Опис",
        max_length=100,
        null=True,
        blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class ObjectType(models.Model):
    name = models.CharField(
        "Назва",
        max_length=30
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип Об'єкту"
        verbose_name_plural = "Типи Об'єктів"


def get_currency():
    default_currency = Currency.objects.get(name="Гривня")
    return default_currency.id


class ObjectProperty(models.Model):

    category_object = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категорія")

    object_type = models.ForeignKey(
        ObjectType,
        on_delete=models.PROTECT,
        verbose_name="Тип Об'єкту")

    title = models.CharField(
        "Назва",
        max_length=70)

    image = FilerImageField(
        verbose_name="Головне зображення",
        null=True,
        blank=True,
        related_name="image_object_total",
        on_delete=models.SET_NULL)

    description = RichTextUploadingField("Опис")

    meta_description = models.TextField(
        "Мета опис",
        max_length=160,
        null=True,
        blank=True)

    cad_num = models.CharField(
        "Кадастровий номер",
        max_length=30,
        null=True,
        blank=True
    )

    locality = models.ForeignKey(
        Locality,
        on_delete=models.PROTECT,
        verbose_name="Населенный пункт")

    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        verbose_name="Район/Массив")

    street = models.ForeignKey(
        Street,
        on_delete=models.PROTECT,
        verbose_name="Вулиця")

    rooms = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        verbose_name="Кількість кімнат",
        null=True,
        blank=True)

    total_space = models.IntegerField(
        "Загальна площа",
        null=True,
        blank=True)

    living_space = models.IntegerField(
        "Житлова площа",
        null=True,
        blank=True)

    kitchen_space = models.IntegerField(
        "Кухня площа",
        null=True,
        blank=True)

    height = models.FloatField(
        "Висота стелі",
        null=True,
        blank=True)

    floor = models.IntegerField(
        "Поверх",
        null=True,
        blank=True)

    storeys = models.ForeignKey(
        Storey,
        on_delete=models.PROTECT,
        verbose_name="Поверховість",
        null=True,
        blank=True
    )

    price = models.IntegerField("Ціна")

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        default=get_currency,
        verbose_name="Валюта")

    published = models.DateField(
        "Створено",
        auto_now_add=True,
        db_index=True)

    recommended = models.BooleanField(
        "Рекомендований",
        default=False)

    status = models.BooleanField(
        "Статус",
        default=True)

    def __str__(self):
        return self.title
    """
    @staticmethod
    def get_object_types(name):

        return (
            'Квартира',
            'Будинок',
            'Земельна ділянка',
            'Дачний масив',
            'Комерційна нерухомість')
    """
    class Meta:
        verbose_name = "Об'єкт"
        verbose_name_plural = "Об'єкти"
        ordering = ['-published']


class ObjectPropertyImage(models.Model):

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Зображення"
        verbose_name_plural = "Додаткові зображення"

    image = FilerImageField(
        null=True,
        blank=True,
        related_name="image_object",
        on_delete=models.SET_NULL)

    object_property = models.ForeignKey(
        ObjectProperty,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Зображення")


class Page(models.Model):
    title = models.CharField(
        "Назва",
        max_length=70)

    image = FilerImageField(
        verbose_name="Головне зображення",
        null=True,
        blank=True,
        related_name="image_page_total",
        on_delete=models.SET_NULL)

    description = RichTextUploadingField("Опис")

    meta_description = models.TextField(
        "Мета опис",
        max_length=160,
        null=True,
        blank=True)

    published = models.DateField(
        "Створено",
        auto_now_add=True,
        db_index=True)

    menu = models.BooleanField(
        "Меню",
        default=False)

    information = models.BooleanField(
        "Підвал (Інформація)",
        default=False)

    about_as = models.BooleanField(
        "Підвал (Про нас)",
        default=False)

    status = models.BooleanField(
        "Статус",
        default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сторінка"
        verbose_name_plural = "Сторінки"
        ordering = ['-published']