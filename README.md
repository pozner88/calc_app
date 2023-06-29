# API калькулятора 

# Запуск в контейнере
Для запуска контейнера с проектом необходимо написать команду:
```bash
$ docker compose up
```
После нее происходит запуск проекта и БД через docker compose и появляется возможность подключиться к проекту 
по адресу http://127.0.0.1:8000/ или http://localhost:1

# Тестирование
Для тестирования проекта необходимо запустить проект в контейнере как указано выше, перейти в папку проекта 
```bash
$ cd app
```
Запустить тестирование с помощью pytest
```bash
$ pytest
```