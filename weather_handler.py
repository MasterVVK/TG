import logging
import aiohttp
from urllib.parse import quote
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

# Функция для получения прогноза погоды
async def get_weather(city_name, weather_api_key):
    city_name_encoded = quote(city_name, safe='')
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city_name_encoded}&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            logging.debug(f"Запрос к WeatherAPI: {response.url}")
            if response.status == 200:
                data = await response.json()
                logging.debug(f"Ответ от WeatherAPI: {data}")
                if 'current' in data:
                    weather_description = data['current']['condition']['text']
                    temperature = data['current']['temp_c']
                    humidity = data['current']['humidity']
                    icon_url = "http:" + data['current']['condition']['icon']
                    return f"Погода в городе {city_name}:\nТемпература: {temperature}°C\nОписание: {weather_description}\nВлажность: {humidity}%", icon_url
            else:
                logging.error(f"Ошибка при запросе к WeatherAPI: {response.status} {await response.text()}")
                return None, None

# Команда /weather
@router.message(Command("weather"))
async def send_weather(message: Message):
    logging.info("Получена команда /weather")
    args = message.text.split(' ', 1)
    city_name = args[1] if len(args) > 1 else "Москва"  # Установите значение по умолчанию

    weather_api_key = "YOUR_WEATHER_API_KEY"  # Укажите ваш ключ API
    weather, icon_url = await get_weather(city_name, weather_api_key)
    if weather and icon_url:
        logging.info(f"Отправка прогноза погоды: {weather}")
        await message.answer_photo(photo=icon_url, caption=weather)
    else:
        logging.warning(f"Не удалось получить данные о погоде для города: {city_name}")
        await message.reply("Не удалось получить данные о погоде. Попробуйте позже.")
