from django.contrib import admin
from django.shortcuts import reverse
from django.templatetags.static import static
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpResponseRedirect
from .models import Product
from .models import ProductCategory
from .models import Restaurant
from .models import RestaurantMenuItem
from .models import Order
from .models import OrderElements
from banners.models import Banner, Page
from django.utils.html import format_html, mark_safe
from adminsortable2.admin import SortableInlineAdminMixin


class BannerImageSortableAdmin(admin.TabularInline, SortableInlineAdminMixin):
    model = Banner
    readonly_fields = "image_preview",

    def image_preview(self, image):

        response = format_html("<img src={} width=200>", mark_safe(image.image.url))

        return response


@admin.register(Page)
class AdminPage(admin.ModelAdmin):

    inlines = [BannerImageSortableAdmin]

    class Meta:
        model = Page


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass


class RestaurantMenuItemInline(admin.TabularInline):
    model = RestaurantMenuItem
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'address',
        'contact_phone',
    ]
    list_display = [
        'name',
        'address',
        'contact_phone',
    ]
    inlines = [
        RestaurantMenuItemInline
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'get_image_list_preview',
        'name',
        'category',
        'price',
    ]
    list_display_links = [
        'name',
    ]
    list_filter = [
        'category',
    ]
    search_fields = [
        # FIXME SQLite can not convert letter case for cyrillic words properly, so search will be buggy.
        # Migration to PostgreSQL is necessary
        'name',
        'category__name',
    ]

    inlines = [
        RestaurantMenuItemInline
    ]
    fieldsets = (
        ('Общее', {
            'fields': [
                'name',
                'category',
                'image',
                'get_image_preview',
                'price',
            ]
        }),
        ('Подробно', {
            'fields': [
                'special_status',
                'description',
            ],
            'classes': [
                'wide'
            ],
        }),
    )

    readonly_fields = [
        'get_image_preview',
    ]

    class Media:
        css = {
            "all": (
                static("admin/foodcartapp.css")
            )
        }

    def get_image_preview(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)
    get_image_preview.short_description = 'превью'

    def get_image_list_preview(self, obj):
        if not obj.image or not obj.id:
            return 'нет картинки'
        edit_url = reverse('admin:foodcartapp_product_change', args=(obj.id,))
        return format_html('<a href="{edit_url}"><img src="{src}" style="max-height: 50px;"/></a>', edit_url=edit_url, src=obj.image.url)
    get_image_list_preview.short_description = 'превью'


@admin.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):
    pass


class OrderElementsAdmin(admin.StackedInline):
    model = OrderElements


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderElementsAdmin
    ]

    list_display = ['lastname', 'address', 'phonenumber', 'price']
    list_filter = ('lastname', 'address')
    readonly_fields = ('price',)

    def price(self, obj):
        return obj.price

    price.short_description = 'цена'

    def get_queryset(self, request):
        queryset = super().get_queryset(request).with_price()
        return queryset

    def response_change(self, request, obj):
        response = super().response_change(request, obj)
        if 'next' in request.GET:
            is_url_safe = url_has_allowed_host_and_scheme(url=request.GET['next'], allowed_hosts=None)
            if is_url_safe:
                return HttpResponseRedirect(request.GET['next'])
        else:
            return response

    class Meta:
        model = Order


@admin.register(OrderElements)
class OrderElements(admin.ModelAdmin):
    raw_id_fields = ['order', 'product']
