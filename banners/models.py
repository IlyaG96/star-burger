from django.db import models


def get_file_path(instance, filename):
    return f'banners/{filename}'


class Page(models.Model):
    name = models.CharField(
        max_length=255
    )

    def __str__(self):
        return f'Баннеры со страницы {self.name} '

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'


class Banner(models.Model):

    page = models.ForeignKey(
        'Page',
        verbose_name='относится к странице',
        related_name='page',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    order_number = models.PositiveSmallIntegerField(
        'порядковый номер',
    )

    description = models.CharField(
        'Текст-описание',
        max_length=50,
        blank=True,
    )

    image = models.ImageField(
        'Картинка',
        upload_to=get_file_path,
        blank=True,
    )

    def __str__(self):
        return f'{self.order_number} картинка со страницы {self.page.name}'

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['order_number']

