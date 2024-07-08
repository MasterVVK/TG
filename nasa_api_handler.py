# nasa_api_handler.py

import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import json
import logging
from googletrans import Translator

router = Router()

# Загрузка конфигурации из файла config.json
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

NASA_API_KEY = config['NASA_API_KEY']

translator = Translator()

@router.message(Command("nasa"))
async def send_nasa_apod(message: Message):
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}'
    response = requests.get(url)
    logging.debug(f"Запрос к NasaAPI: {response.url}")
    if response.status_code == 200:
        data = response.json()
        apod_url = data['url']
        title = data['title']
        explanation = data['explanation']

        # Перевод названия и объяснения на русский язык
        title_ru = translator.translate(title, dest='ru').text
        explanation_ru = translator.translate(explanation, dest='ru').text

        await message.reply_photo(photo=apod_url, caption=title_ru)

        # Разбиваем описание на части, если оно слишком длинное
        parts = [explanation_ru[i:i + 1024] for i in range(0, len(explanation_ru), 1024)]
        for part in parts:
            await message.reply(part)
    else:
        await message.reply("Не удалось получить данные от NASA. Попробуйте позже.")
