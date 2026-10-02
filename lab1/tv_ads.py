# Лабораторная работа №1. Вариант 25.
# Учёт телекомпанией стоимости прошедшей в эфире рекламы.
# Фильтрация рекламных агентов по размеру зарплаты.

# Передачи: рейтинг и стоимость минуты рекламы (руб.)
programs = {
    "Новости дня":          {"rating": 8.7, "price_per_min": 90000},
    "Вечерний сериал":      {"rating": 7.5, "price_per_min": 75000},
    "Футбольное обозрение": {"rating": 6.1, "price_per_min": 55000},
    "Утро с нами":          {"rating": 4.2, "price_per_min": 30000},
    "Кулинарный час":       {"rating": 3.8, "price_per_min": 25000},
}

# Рекламные агенты и ролики, прошедшие в эфире по их договорам
# (duration – продолжительность ролика в секундах)
agents = [
    {
        "name": "Алексей",
        "surname": "Орлов",
        "phone": "+7 (495) 111-22-33",
        "percent": 5,
        "ads": [
            {"customer": "ООО «Ромашка»", "program": "Новости дня",
             "date": "2026-09-01", "duration": 30},
            {"customer": "ООО «Ромашка»", "program": "Вечерний сериал",
             "date": "2026-09-02", "duration": 20},
            {"customer": "АО «ТехноСвязь»", "program": "Новости дня",
             "date": "2026-09-03", "duration": 45},
        ]
    },
    {
        "name": "Ольга",
        "surname": "Белова",
        "phone": "+7 (495) 222-33-44",
        "percent": 7,
        "ads": [
            {"customer": "ИП Сидоров", "program": "Кулинарный час",
             "date": "2026-09-01", "duration": 15},
            {"customer": "ООО «Вкусный дом»", "program": "Утро с нами",
             "date": "2026-09-04", "duration": 30},
        ]
    },
    {
        "name": "Сергей",
        "surname": "Кравцов",
        "phone": "+7 (495) 333-44-55",
        "percent": 6,
        "ads": [
            {"customer": "ООО «СпортМаркет»", "program": "Футбольное обозрение",
             "date": "2026-09-05", "duration": 60},
            {"customer": "ООО «СпортМаркет»", "program": "Новости дня",
             "date": "2026-09-06", "duration": 30},
        ]
    },
    {
        "name": "Наталья",
        "surname": "Громова",
        "phone": "+7 (495) 444-55-66",
        "percent": 5,
        "ads": [
            {"customer": "АО «АвтоМир»", "program": "Вечерний сериал",
             "date": "2026-09-02", "duration": 40},
            {"customer": "АО «АвтоМир»", "program": "Вечерний сериал",
             "date": "2026-09-09", "duration": 40},
            {"customer": "ООО «Ромашка»", "program": "Утро с нами",
             "date": "2026-09-10", "duration": 20},
        ]
    },
    {
        "name": "Игорь",
        "surname": "Лебедев",
        "phone": "+7 (495) 555-66-77",
        "percent": 8,
        "ads": [
            {"customer": "ИП Ковалёва", "program": "Кулинарный час",
             "date": "2026-09-07", "duration": 20},
        ]
    },
]


def ad_cost(ad):
    """Стоимость ролика = продолжительность (мин) * стоимость минуты в передаче."""
    price = programs[ad["program"]]["price_per_min"]
    return ad["duration"] / 60 * price


def total_cost(agent):
    """Общая стоимость рекламы агента, прошедшей в эфире."""
    return sum(ad_cost(ad) for ad in agent["ads"])


def salary(agent):
    """Зарплата агента – процент от общей стоимости рекламы."""
    return total_cost(agent) * agent["percent"] / 100


def print_programs():
    """Выводит таблицу передач."""
    print(u"Передача".ljust(24), u"Рейтинг".ljust(9), u"Цена минуты, руб.")
    for name, info in programs.items():
        print(name.ljust(24), str(info["rating"]).ljust(9), info["price_per_min"])


def print_agents(agent_list):
    """Выводит таблицу рекламных агентов."""
    print(u"Имя".ljust(10), u"Фамилия".ljust(10), u"Телефон".ljust(20),
          u"Роликов".ljust(8), u"Стоимость, руб.".ljust(16),
          u"%".ljust(4), u"Зарплата, руб.")
    for agent in agent_list:
        print(agent["name"].ljust(10),
              agent["surname"].ljust(10),
              agent["phone"].ljust(20),
              str(len(agent["ads"])).ljust(8),
              f"{total_cost(agent):.2f}".ljust(16),
              str(agent["percent"]).ljust(4),
              f"{salary(agent):.2f}")


def filter_agents(agent_list, min_salary):
    """Возвращает агентов, зарплата которых выше min_salary."""
    return [a for a in agent_list if salary(a) > min_salary]


def read_min_salary():
    """Считывает с клавиатуры порог зарплаты (допускается точка и запятая)."""
    while True:
        value = input("Введите размер зарплаты для фильтрации, руб.: ")
        try:
            number = float(value.replace(",", ".").replace(" ", ""))
        except ValueError:
            print("Ошибка: введите число, например 5000 или 7500,50")
            continue
        if number >= 0:
            return number
        print("Ошибка: зарплата не может быть отрицательной")


print("Передачи телекомпании:")
print_programs()
print()
print("Рекламные агенты:")
print_agents(agents)
print()

min_salary = read_min_salary()
result = filter_agents(agents, min_salary)

print()
if result:
    print(f"Агенты с зарплатой выше {min_salary:.2f} руб.:")
    print_agents(result)
else:
    print(f"Агентов с зарплатой выше {min_salary:.2f} руб. нет.")
