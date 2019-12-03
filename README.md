# Project test

## Общее описание
Тестовый проект представлет собой приложение, которое имитирует взаимодействие сервера с клиентами через АПИ ключ. Пользователь (User django) может создавать неограниченное количество приложений(через API) и получать АПИ ключ уникальный для каждого.
Создан тестовый endpoint, который требует наличие АПИ ключа для возвращения информации по данному приложению. Для реализации АПИ ключа было выбранно https://florimondmanca.github.io/djangorestframework-api-key/. Из преимуществ перед кастомной реалицазии:
1. Наличие документации
2. Покрыто тестами
3. Наличие дополнительных фич, которые могут быть полезны в будущем: revoke ключ, ограничение ключа по времени жизни, throttling etc.

## Пункты инструкции
1. Как авторизоваться? Используется стандартный класс DRF для авторизации https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication
2. Как добавить, удалить и тд? Для предоставления api endpoints класс GenericViewSet (автоматическая генерация урлов для CRUD). В урлы заложена версионность '/api/v1/'. Все эндпоинты покрыты юнит тестами.
3. Стандартные CRUD расширен 2 методами regenerate_token (для пересоздания апи ключа) и test (для проверки работы апи ключа)
4. Все эндпоинты кроме /test/ требуют авторизацию юзера, /test/ использует свой permission класс для работы с апи ключем.


## Start docker 
1\. add .env to root project folder (see .env_example)
```
$ cp .env_example .env
```

2\. build
```
$ docker-compose -f docker-compose.local.yml build --no-cache
```

3\. run
```
$ docker-compose -f docker-compose.local.yml up -d
```

run django commands:
```
$ make manage.py f=docker-compose.local.yml cmd=migrate
$ make manage.py f=docker-compose.local.yml cmd=createsuperuser
```

## Run tests
```
make manage.py f=docker-compose.local.yml cmd='test applications --keepdb'
```
