##  Техническое задание
Задача: Создать клиент-серверное приложение на сокетах (asyncio, консольное приложение) менеджер виртуальных машин. Должен быть написан как сервер, так и клиент, работа должна быть продемонстрирована в виде нескольких подключений клиентов к серверу. Сервер должен как принимать команды от клиентов, так и обрабатывать свои внутренние команды.

## Логика приложения 
Данный проект включает в себя простого менеджера виртуальных машин, представляющего TCP-сервер с API и клиентский сервер, как интерфейс для управления машинами.
На сервере интегрирована аутентификация, и клиенты способны управлять своими группами ВМ через разные консоли.

## Стек технологий
<div align="center">
   <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />
   <img src='https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white' />
   <img src="https://img.shields.io/badge/Docker-9999FF.svg?style=for-the-badge&logo=Docker&logoColor=white" />
   <img src="https://img.shields.io/badge/VS%20Code%20Insiders-35b393.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white" />
</div>

## Установка
1. Клоним репозиторий:
```
git init
git clone https://github.com/John321Blacksmith/Red-Soft-task-assigment.git
```

2. Для взаимодействия ВМ-менеджера с postgres контейнером, в директории проекта необходимо
   создать **.env** файл и указать конфигурации:   
```
PGUSER='your name'
PGPASSWORD='yourpassword321'
PGHOST='localhost'
PGPORT='5432'
PGDATABASE='vm_management'
```
3. Устанавливаем виртуальную среду и необходимые зависимости:
```
python -m venv .venv
.venv\Scripts\activate

# linux
source .venv/bin/activate

pip install -r requirements.txt
```

4. Перед запуском инструкции, убедитесь, что Docker машина запущена.
   В compose файле, укажите те же конфигурации, что и в окружении.
   Инициализируем образ:
```
docker compose --build
```

5. Поднимаем контейнер с postgres:
```
# 
# Запуск в фоновом режиме
docker compose up -d

# Запуск с логами
docker compose up
```

## Запуск движка

1. Вводим:
```
python server_side/launch.py
```

## Запуск одного и более клиентов
1. Открываем новую консоль.

3. Активируем окружение и переходим на клиетскую директорию:
```
# win
.venv\Scripts\activate

# linux
source .venv/bin/activate

cd client_app
```

3. Запускаем консольную программу:
```
python client.py
```
