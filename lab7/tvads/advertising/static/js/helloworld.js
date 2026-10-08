// Лабораторная работа №7. Вариант 25.
// Учёт телекомпанией стоимости прошедшей в эфире рекламы.

// Стоимость минуты рекламы в передачах (руб.), определяется по рейтингу
var programs = {
    "Новости дня": 90000,
    "Вечерний сериал": 75000,
    "Футбольное обозрение": 55000,
    "Утро с нами": 30000,
    "Кулинарный час": 25000
};

// Рекламные агенты и ролики, прошедшие в эфире по их договорам
// (duration – продолжительность ролика в секундах)
var agents = [
    {
        "name": "Алексей",
        "surname": "Орлов",
        "percent": 5,
        "ads": [
            {"customer": "ООО «Ромашка»", "program": "Новости дня", "duration": 30},
            {"customer": "ООО «Ромашка»", "program": "Вечерний сериал", "duration": 20},
            {"customer": "АО «ТехноСвязь»", "program": "Новости дня", "duration": 45}
        ]
    },
    {
        "name": "Ольга",
        "surname": "Белова",
        "percent": 7,
        "ads": [
            {"customer": "ИП Сидоров", "program": "Кулинарный час", "duration": 15},
            {"customer": "ООО «Вкусный дом»", "program": "Утро с нами", "duration": 30}
        ]
    },
    {
        "name": "Сергей",
        "surname": "Кравцов",
        "percent": 6,
        "ads": [
            {"customer": "ООО «СпортМаркет»", "program": "Футбольное обозрение", "duration": 60},
            {"customer": "ООО «СпортМаркет»", "program": "Новости дня", "duration": 30}
        ]
    },
    {
        "name": "Наталья",
        "surname": "Громова",
        "percent": 5,
        "ads": [
            {"customer": "АО «АвтоМир»", "program": "Вечерний сериал", "duration": 40},
            {"customer": "АО «АвтоМир»", "program": "Вечерний сериал", "duration": 40},
            {"customer": "ООО «Ромашка»", "program": "Утро с нами", "duration": 20}
        ]
    },
    {
        "name": "Игорь",
        "surname": "Лебедев",
        "percent": 8,
        "ads": [
            {"customer": "ИП Ковалёва", "program": "Кулинарный час", "duration": 20}
        ]
    }
];

console.log(agents);

// Аналог метода ljust из Python: дополняет строку пробелами справа
var rpad = function(str, length) {
    str = str.toString();
    while (str.length < length)
        str = str + ' ';
    return str;
};

// Стоимость ролика = продолжительность (мин) * стоимость минуты в передаче
var adCost = function(ad) {
    return ad.duration / 60 * programs[ad.program];
};

// Общая стоимость рекламы агента, прошедшей в эфире
var totalCost = function(agent) {
    var sum = 0;
    for (var i = 0; i < agent.ads.length; i++)
        sum += adCost(agent.ads[i]);
    return sum;
};

// Зарплата агента – процент от общей стоимости рекламы
var salary = function(agent) {
    return totalCost(agent) * agent.percent / 100;
};

var printAgents = function(list) {
    console.log(
        rpad("Имя", 10), rpad("Фамилия", 10), rpad("Роликов", 8),
        rpad("Стоимость", 12), rpad("%", 4), rpad("Зарплата", 10)
    );
    for (var i = 0; i <= list.length - 1; i++) {
        console.log(
            rpad(list[i]['name'], 10),
            rpad(list[i]['surname'], 10),
            rpad(list[i]['ads'].length, 8),
            rpad(totalCost(list[i]).toFixed(2), 12),
            rpad(list[i]['percent'], 4),
            rpad(salary(list[i]).toFixed(2), 10)
        );
    }
    console.log('\n');
};

var printAds = function(list) {
    console.log(
        rpad("Агент", 18), rpad("Заказчик", 20), rpad("Передача", 22),
        rpad("Длит., с", 9), rpad("Стоимость", 10)
    );
    for (var i = 0; i < list.length; i++) {
        console.log(
            rpad(list[i].agent, 18), rpad(list[i].customer, 20),
            rpad(list[i].program, 22), rpad(list[i].duration, 9),
            rpad(adCost(list[i]).toFixed(2), 10)
        );
    }
    console.log('\n');
};

// Задание 1 (аналог фильтрации по группе):
// ролики, прошедшие в эфире в передаче, название которой вводит пользователь
var filterByProgram = function(list, program) {
    var result = [];
    for (var i = 0; i < list.length; i++) {
        for (var j = 0; j < list[i].ads.length; j++) {
            var ad = list[i].ads[j];
            if (ad.program.toLowerCase() == program.toLowerCase()) {
                result.push({
                    "agent": list[i].name + " " + list[i].surname,
                    "customer": ad.customer,
                    "program": ad.program,
                    "duration": ad.duration
                });
            }
        }
    }
    return result;
};

// Задание 2 (аналог фильтрации по среднему баллу):
// агенты, зарплата которых выше значения, введённого пользователем
var filterBySalary = function(list, minSalary) {
    return list.filter(function(agent) {
        return salary(agent) > minSalary;
    });
};

console.log("Все рекламные агенты:");
printAgents(agents);

var program = prompt("Введите название передачи:", "Новости дня");
if (program !== null && program.trim() !== "") {
    program = program.trim();
    var byProgram = filterByProgram(agents, program);
    if (byProgram.length > 0) {
        console.log("Ролики в передаче «" + program + "»:");
        printAds(byProgram);
    } else {
        console.log("Роликов в передаче «" + program + "» нет.\n");
    }
}

var input = prompt("Введите размер зарплаты для фильтрации, руб.:", "5000");
var minSalary = parseFloat(String(input).replace(",", ".").replace(/\s/g, ""));
if (isNaN(minSalary) || minSalary < 0) {
    console.log("Ошибка: размер зарплаты должен быть неотрицательным числом.");
} else {
    var bySalary = filterBySalary(agents, minSalary);
    if (bySalary.length > 0) {
        console.log("Агенты с зарплатой выше " + minSalary.toFixed(2) + " руб.:");
        printAgents(bySalary);
    } else {
        console.log("Агентов с зарплатой выше " + minSalary.toFixed(2) + " руб. нет.");
    }
}
