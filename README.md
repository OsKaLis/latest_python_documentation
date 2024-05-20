<div id="header" align="center">
  <h1>Проект latest_python_documentation</h1>
</div>

## Что это за проект, какую задачу он решает, в чём его польза:
> [!NOTE]
> Проект предназначин для парсинга свежей документации python.

## Как развернуть проект на локальной машине.
> [!IMPORTANT]
> * [1] (Клонируем проект) :git clone git@github.com:OsKaLis/latest_python_documentation.git
> * [2] (Переходим в директорию проекта) :cd latest_python_documentation/
> * [3] (Устанавливаем виртуальное окружение) :python -m venv venv
> * [4] (Запускаем виртуальное окружение из папки "latest_python_documentation") :source venv/Scripts/activate
> * [5] (Установка всех нужных библиотек) :pip install -r requirements.txt
> * [6] (Переходим в директорию "src" ) :cd src/
> * [7] (Запускаем main,py с параметрами или без ) :python main.py {параметры}

## Cтек технологий:
<img src="https://img.shields.io/badge/Python_-3.9.10-Green"> <img src="https://img.shields.io/badge/BeautifulSoup_-4.9.3-blue"> <img src="https://img.shields.io/badge/tqdm_-4.61.0-red">
<img src="https://img.shields.io/badge/prettytable_-2.1.0-aqua">

## Некоторые примеры терминала.

### Простое использование вывод в кансоль:
* python main.py whats-new

### Вывод информации с помощью таблицы:
* python main.py latest-versions --output pretty

### Сохранение информации в ваил "csv" в папке "results":
* python main.py pep -o file

## Справка вызывается:
* python main.py -h

## Автор: Юшко Ю.Ю.
