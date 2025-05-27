# Запуск приложения

1. `py -m venv venv` - установка виртуальной среды
2. `venv\Scripts\activate.bat` - запуск среды
3. `pip install -r requirements.txt` - установка библиотек
4. `py manage.py migrate` - создание базы
5. `py manage.py createsuperuser` - создание админа (его изначально нет)
6. `py manage.py runserver` - запуск сайта
