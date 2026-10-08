from datetime import date
from decimal import Decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import Http404
from django.shortcuts import redirect, render

from .models import Advertisement, Agent, Customer, Program


def archive(request):
    return render(request, 'archive.html',
                  {"posts": Advertisement.objects.all()})


def get_ad(request, ad_id):
    try:
        post = Advertisement.objects.get(id=ad_id)
        return render(request, 'ad.html', {"post": post})
    except Advertisement.DoesNotExist:
        raise Http404


def create_ad(request):
    # Создавать ролики может только авторизованный пользователь
    if request.user.is_anonymous:
        raise Http404

    # ...и только если его учётная запись связана с рекламным агентом
    try:
        agent = request.user.agent
    except Agent.DoesNotExist:
        return render(request, 'create_ad.html', {'not_agent': True})

    context = {
        'customers': Customer.objects.all(),
        'programs': Program.objects.all(),
    }

    if request.method == "POST":
        # обработать данные формы, если метод POST
        fields = ('title', 'customer', 'program', 'air_date',
                  'duration', 'description')
        form = {name: request.POST.get(name, '').strip() for name in fields}
        errors = []

        if not all(form.values()):
            errors.append("Не все поля заполнены")
        else:
            # проверка уникальности названия ролика
            if Advertisement.objects.filter(title__iexact=form['title']).exists():
                errors.append("Ролик с таким названием уже существует")

            if not form['duration'].isdigit() or int(form['duration']) == 0:
                errors.append("Продолжительность должна быть целым "
                              "положительным числом секунд")

            try:
                air_date = date.fromisoformat(form['air_date'])
            except ValueError:
                errors.append("Некорректная дата выхода в эфир")

            customer = Customer.objects.filter(
                id=form['customer']).first() if form['customer'].isdigit() else None
            program = Program.objects.filter(
                id=form['program']).first() if form['program'].isdigit() else None
            if customer is None:
                errors.append("Выберите заказчика из списка")
            if program is None:
                errors.append("Выберите передачу из списка")

        if errors:
            # если введённые данные некорректны – вернуть форму с ошибками
            form['errors'] = errors
            context['form'] = form
            return render(request, 'create_ad.html', context)

        # если поля заполнены без ошибок – сохранить ролик
        ad = Advertisement.objects.create(
            title=form['title'],
            customer=customer,
            program=program,
            agent=agent,
            air_date=air_date,
            duration=int(form['duration']),
            description=form['description'],
        )
        # перейти на страницу созданного ролика
        return redirect('get_ad', ad_id=ad.id)

    # просто вернуть страницу с формой, если метод GET
    return render(request, 'create_ad.html', context)


# Процент вознаграждения, назначаемый новому агенту при регистрации.
# Руководитель коммерческой службы может изменить его в админке.
DEFAULT_PERCENT = Decimal('5.00')


def register(request):
    if request.user.is_authenticated:
        return redirect('archive')

    if request.method == "POST":
        fields = ('username', 'first_name', 'last_name', 'email', 'phone',
                  'password', 'password2')
        form = {name: request.POST.get(name, '').strip() for name in fields}
        errors = []

        if not all(form.values()):
            errors.append("Не все поля заполнены")
        else:
            # проверка уникальности логина
            try:
                User.objects.get(username=form['username'])
                errors.append("Пользователь с таким логином уже существует")
            except User.DoesNotExist:
                pass

            try:
                validate_email(form['email'])
            except ValidationError:
                errors.append("Некорректный адрес электронной почты")

            if len(form['password']) < 8:
                errors.append("Пароль должен содержать не менее 8 символов")
            if form['password'] != form['password2']:
                errors.append("Пароли не совпадают")

        if errors:
            # пароли обратно в форму не возвращаем
            form['password'] = form['password2'] = ''
            form['errors'] = errors
            return render(request, 'register.html', {'form': form})

        user = User.objects.create_user(form['username'], form['email'],
                                        form['password'])
        user.first_name = form['first_name']
        user.last_name = form['last_name']
        user.save()
        Agent.objects.create(user=user, phone=form['phone'],
                             percent=DEFAULT_PERCENT)

        login(request, user)
        return redirect('archive')

    return render(request, 'register.html', {})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('archive')

    if request.method == "POST":
        form = {
            'username': request.POST.get('username', '').strip(),
            'password': request.POST.get('password', ''),
        }
        if not form['username'] or not form['password']:
            form['errors'] = "Не все поля заполнены"
        else:
            user = authenticate(username=form['username'],
                                password=form['password'])
            if user is not None:
                login(request, user)
                return redirect('archive')
            form['errors'] = ("Аккаунт с таким логином и паролем "
                              "не существует")
        form['password'] = ''
        return render(request, 'login.html', {'form': form})

    return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    return redirect('archive')
