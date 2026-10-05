from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Program(models.Model):
    """Телепередача."""
    name = models.CharField('Название', max_length=200)
    rating = models.DecimalField('Рейтинг', max_digits=4, decimal_places=1)
    price_per_minute = models.DecimalField('Стоимость минуты рекламы, руб.',
                                           max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Передача'
        verbose_name_plural = 'Передачи'

    def __str__(self):
        return self.name


class Customer(models.Model):
    """Организация-заказчик рекламы."""
    name = models.CharField('Организация', max_length=200)
    inn = models.CharField('ИНН', max_length=12)
    bank_name = models.CharField('Банк', max_length=200)
    bank_account = models.CharField('Расчётный счёт', max_length=20)
    phone = models.CharField('Телефон', max_length=30)
    contact_person = models.CharField('Контактное лицо', max_length=200)

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return self.name


class Agent(models.Model):
    """Рекламный агент (связан с учётной записью пользователя)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    phone = models.CharField('Телефон', max_length=30)
    percent = models.DecimalField('Процент от стоимости рекламы',
                                  max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Рекламный агент'
        verbose_name_plural = 'Рекламные агенты'

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def get_total_cost(self):
        """Общая стоимость рекламы агента, уже прошедшей в эфире."""
        aired = self.advertisement_set.filter(air_date__lte=date.today())
        return sum((ad.get_cost() for ad in aired), Decimal('0.00'))
    get_total_cost.short_description = 'Реклама в эфире, руб.'

    def get_salary(self):
        """Зарплата агента – процент от стоимости прошедшей в эфире рекламы."""
        salary = self.get_total_cost() * self.percent / 100
        return salary.quantize(Decimal('0.01'))
    get_salary.short_description = 'Зарплата, руб.'


class Advertisement(models.Model):
    """Рекламный ролик, размещённый в передаче в определённый день."""
    title = models.CharField('Название ролика', max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 verbose_name='Заказчик')
    program = models.ForeignKey(Program, on_delete=models.CASCADE,
                                verbose_name='Передача')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE,
                              verbose_name='Агент')
    air_date = models.DateField('Дата выхода в эфир')
    duration = models.PositiveIntegerField('Продолжительность, с')
    description = models.TextField('Описание ролика')
    created_date = models.DateField('Дата договора', auto_now_add=True)

    class Meta:
        verbose_name = 'Рекламный ролик'
        verbose_name_plural = 'Рекламные ролики'
        ordering = ['air_date']

    def __str__(self):
        return "%s: %s" % (self.customer.name, self.title)

    def get_cost(self):
        """Стоимость ролика = продолжительность (мин) * стоимость минуты."""
        cost = self.program.price_per_minute * self.duration / 60
        return cost.quantize(Decimal('0.01'))
    get_cost.short_description = 'Стоимость, руб.'

    def is_aired(self):
        return self.air_date <= date.today()
    is_aired.boolean = True
    is_aired.short_description = 'В эфире'

    def get_excerpt(self):
        if len(self.description) > 140:
            return self.description[:140] + "..."
        return self.description
    get_excerpt.short_description = 'Описание'
