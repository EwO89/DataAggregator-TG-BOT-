# DataAggregator-TG-BOT-

### ТЗ можно посмотреть тут > https://drive.google.com/drive/folders/1fcXvOXHapAKmfchQRVKPGy2FhOtj-XHZ?usp=sharing

## Обзор
**DataAggregator-TG-BOT** - это Telegram-бот, предназначенный для взаимодействия с MongoDB для агрегирования и получения данных на основе запросов пользователей. Этот бот может обрабатывать команды пользователей для выполнения агрегации данных и предоставления результатов в структурированном формате.

## Функциональные возможности
- **Команда /start** для инициализации взаимодействия с пользователем.
- **JSON-запросы** для получения агрегированных данных.
- **Использование MongoDB** для хранения данных пользователей и выполнения агрегаций.
- **Автоматическое создание индексов** на указанных полях для оптимизации запросов.

## Настройка и запуск
Предварительные требования:
- Python 3.12
- Docker и Docker Compose
- MongoDB (локальный или удаленный)
  
**Переменные окружения**

Создайте файл .env в корневом каталоге проекта с следующими переменными:
```
MONGODB_URI=your_mongodb_uri
MONGODB_DB=your_database_name
USERS_COLLECTION=users_collection_name
DATA_COLLECTION=data_collection_name
TOKEN=your_telegram_bot_token
```
**Установка зависимостей**

Этот проект использует Poetry для управления зависимостями. Для установки Poetry следуйте инструкциям на сайте Poetry.

**Установите зависимости**
```
poetry install
```
**Для запуска приложения локально - активируйте виртуальное окружение**
```
poetry shell
```
**Запустите бота**
```
python src/app.py
```
**Запуск бота с помощью Docker**
```
docker-compose up --build
```
**Команда /start**

/start: Инициализирует взаимодействие пользователя и сервера (тг бота) и сохраняет информацию о пользователе в бд.

**JSON-запрос**

Отправьте JSON-сообщение боту для получения агрегированных данных (см тз):
```
{
    "dt_from": "2022-09-01T00:00:00",
    "dt_upto": "2022-12-31T23:59:00",
    "group_type": "month"
}
```

