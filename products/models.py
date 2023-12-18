from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.urls import reverse

User = get_user_model()


class Item(models.Model):
    """Модель продукта"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
    

class Discount(models.Model):
    """Модель скидок"""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    value = models.IntegerField(
        verbose_name='Размер скидки'
    )

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return str(self.name) + ' скидка ' + f'{self.value}%'


class Tax(models.Model):
    """Модель налогов"""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    value = models.IntegerField(
        verbose_name='Размер налога'
    )

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'

    def __str__(self):
        return str(self.name) + ' налог ' + f'{self.value}%'


class Order(models.Model):
    """Модель заказа"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Пользователь'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    tax = models.ForeignKey(
        Tax,
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_DEFAULT,
        verbose_name='Налог'
    )
    discount = models.ForeignKey(
        Discount,
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_DEFAULT,
        verbose_name='Скидка',
    )
        

    def get_total_price(self):
        total = sum(item.get_total_cost() for item in self.items.all())
        if self.tax:
            total += total * self.tax.value / 100
        if self.discount:
            total -= total * self.discount.value / 100
        return total

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    """Модель элемента заказа"""
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    item = models.ForeignKey(
        Item,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return str(self.item)

    def get_total_cost(self):
        return self.item.price * self.quantity
