# cat_api_handler.py

import requests
from aiogram import Router, F
from aiogram.types import Message
import json
from aiogram.filters import Command
import logging

router = Router()

# Загрузка конфигурации из файла config.json
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

CAT_API_KEY = config['CAT_API_KEY']

@router.message(Command("cat"))
async def send_cat_image(message: Message):
    url = f'https://api.thecatapi.com/v1/images/search?api_key={CAT_API_KEY}&include_breeds=true'
    response = requests.get(url)
    logging.debug(f"Запрос к TheCatAPI: {response.url}")
    if response.status_code == 200:
        data = response.json()
        logging.debug(f"Ответ от TheCatAPI: {data}")
        cat_image_url = data[0]['url']
        breeds = data[0].get('breeds', [])
        if breeds:
            breed_info = breeds[0]
            breed_name = breed_info['name']
            breed_description = breed_info['description']
            caption = f"Порода: {breed_name}\n\nОписание: {breed_description}"
        else:
            caption = "Не удалось определить породу этой кошки."
        await message.reply_photo(photo=cat_image_url, caption=caption)
    else:
        await message.reply("Не удалось получить изображение кота. Попробуйте позже.")
