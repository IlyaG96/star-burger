from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum, F
from django.utils import timezone
from geoapp.models import GeoData


class RestaurantQueryset(models.QuerySet):

    def with_geo_attributes(self):
        addresses = [restaurant.address for restaurant in self]
        geo_attrs = GeoData.objects.filter(address__in=addresses)
        for restaurant in self:
            restaurant.geodata = list(filter(lambda geo: geo.address == restaurant.address, geo_attrs))[0]

        return self


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    objects = RestaurantQueryset.as_manager()

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def load_geos(self):
        self.geodata = GeoData.objects.filter(address=self.address)
        return self

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
                              .filter(availability=True)
                              .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name='ресторан',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f'{self.restaurant.name} - {self.product.name}'


class OrderQuerySet(models.QuerySet):

    def show_price(self):
        with_price = self.annotate(
            price=Sum(F('elements__price_in_order'))
        )
        return with_price

    def show_available_rests(self):
        restaurants = Restaurant.objects.prefetch_related('menu_items__product').with_geo_attributes()
        all_rests = {}
        for restaurant in restaurants:
            rest_menus = restaurant.menu_items.all()
            menu = [menu.product for menu in rest_menus]
            all_rests[restaurant] = menu

        for order in self:
            available_rests = []
            order_products = [element.product for element in order.elements.select_related('product')]
            for rest, menu in all_rests.items():

                result = all(elem in menu for elem in order_products)
                if result:
                    available_rests.append(rest)

                order.restaurants = available_rests

        return self

    def with_geo_attributes(self):
        addresses = [order.address for order in self]
        geo_attrs = GeoData.objects.filter(address__in=addresses)
        for order in self:
            order.geodata = list(filter(lambda geo: geo.address == order.address, geo_attrs))[0]

        return self


class Order(models.Model):
    ORDER_STATUSES = (
        ('Необработанный', 'Необработанный'),
        ('Обработан', 'Обработан'),
        ('Готовится', 'Готовится'),
        ('Доставляется', 'Доставляется'),
        ('Выполнен', 'Выполнен'),
    )

    PAYMENT = (
        ('Наличностью', 'Наличностью'),
        ('Электронно', 'Электронно'),
        ('Не выбрано', 'Не выбрано'),
    )

    firstname = models.CharField(
        'Имя',
        max_length=100,
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=100
    )
    phonenumber = PhoneNumberField(
        'Номер телефона',
        db_index=True
    )
    address = models.CharField(
        'Адрес',
        max_length=255,
        db_index=True
    )
    status = models.CharField(
        'Cтатус',
        choices=ORDER_STATUSES,
        db_index=True,
        max_length=25,
        default='Необработанный'
    )
    comments = models.TextField(
        'Комментарии',
        blank=True,
        help_text='Пожелания клиента'
    )
    registered_at = models.DateTimeField(
        'Зарегистрирован в:',
        default=timezone.now,
        db_index=True
    )
    called_at = models.DateTimeField(
        'Менеджер перезвонил в:',
        blank=True,
        null=True,
        default=None,
        db_index=True
    )
    delivered_at = models.DateTimeField(
        'Доставлен в:',
        blank=True,
        null=True,
        default=None,
        db_index=True
    )
    payment = models.CharField(
        'Способ оплаты',
        choices=PAYMENT,
        default='Не выбрано',
        max_length=25,
        db_index=True,
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname}: {self.address}'


class OrderElements(models.Model):

    order = models.ForeignKey(
        'Order',
        related_name='elements',
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        db_index=True
    )
    product = models.ForeignKey(
        'Product',
        related_name='order_elements',
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    price_in_order = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name = 'Составляющая заказа'
        verbose_name_plural = 'Элементы заказов'

    def __str__(self):
        return f'{self.order.id} - {self.product}'
