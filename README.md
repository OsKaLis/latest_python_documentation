# latest_python_documentation
## Что это за проект, какую задачу он решает, в чём его польза:
Проект предназначин для парсинга свежей документации python.

## Как развернуть проект на локальной машине.
```
1  ] (Клонируем проект) :git clone git@github.com:OsKaLis/latest_python_documentation.git
2  ] (Переходим в директорию проекта) :cd latest_python_documentation/
3  ] (Устанавливаем виртуальное окружение) :python -m venv venv
4  ] (Запускаем виртуальное окружение из папки "latest_python_documentation") :source venv/Scripts/activate
5  ] (Установка всех нужных библиотек) :pip install -r requirements.txt
6  ] (Переходим в директорию "src" ) :cd src/
7  ] (Запускаем main,py с параметрами или без ) :python main.py {параметры}
```

## Некоторые примеры индпоинтов.
```
## Простое использование вывод в кансоль:
1  ]  python main.py whats-new
```
```
## Вывод информации с помощью таблицы:
2  ]  python main.py latest-versions --pretty
```
```
## Сохранение информации в ваил "csv" в папке "results":
3  ]  python main.py pep -o file
```
```
## Справка вызывается:
4  ]  python main.py -h
```


## Cтек технологий:
```
1 ] Язык программирования Python
2 ] Дополнительные библиотеки [bs4, tqdm, prettytable]
```

## Автор: Юшко Ю.Ю.
