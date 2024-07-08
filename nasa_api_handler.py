# nasa_api_handler.py
import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import json

router = Router()

# Загрузка конфигурации из файла config.json
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

NASA_API_KEY = config['NASA_API_KEY']


@router.message(Command("nasa"))
async def send_nasa_apod(message: Message):
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        apod_url = data['url']
        title = data['title']
        explanation = data['explanation']

        await message.reply_photo(photo=apod_url, caption=title)

        # Разбиваем описание на части, если оно слишком длинное
        parts = [explanation[i:i + 1024] for i in range(0, len(explanation), 1024)]
        for part in parts:
            await message.reply(part)
    else:
        await message.reply("Не удалось получить данные от NASA. Попробуйте позже.")
