# Telegram Bot with Aiogram

Этот проект представляет собой Telegram-бота, созданного с использованием библиотеки [Aiogram](https://github.com/aiogram/aiogram). Бот поддерживает различные функции, такие как перевод текста, прогноз погоды, регистрация студентов, голосовые сообщения и работа с фотографиями.

## Установка

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Создайте файл `config.json` в корневой директории проекта и добавьте в него необходимые параметры:

    ```json
    {
        "API_TOKEN": "your-telegram-bot-api-token",
        "WEATHER_API_KEY": "your-weather-api-key",
        "DEFAULT_CITY_NAME": "your-default-city"
    }
    ```

## Запуск

Чтобы запустить бота, выполните следующую команду:

```bash
python bot.py
