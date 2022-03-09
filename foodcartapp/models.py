from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum, F


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

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

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

    def show_price_admin(self):
        with_price = self.annotate(
            price=Sum(F('elements__price_in_order'))
        )
        return with_price


class Order(models.Model):

    ORDER_STATUSES = (
        ('Необработанный', 'Необработанный'),
        ('Обработан', 'Обработан'),
        ('Готовится', 'Готовится'),
        ('Доставляется', 'Доставляется'),
        ('Выполнен', 'Выполнен'),
    )

    objects = OrderQuerySet.as_manager()

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
        related_name='order_products',
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=1,
        validators=[MinValueValidator(1)]
    )

    price_in_order = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        null=True
    )

    class Meta:
        verbose_name = 'Составляющая заказа'
        verbose_name_plural = 'Элементы заказов'

    def __str__(self):
        return f'{self.order.id} - {self.product}'
