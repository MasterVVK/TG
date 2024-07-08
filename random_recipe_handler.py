# random_recipe_handler.py

import requests
import json
import html2text
from googletrans import Translator
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

# Загрузка конфигурации из файла config.json с явным указанием кодировки utf-8
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

SPOONACULAR_API_KEY = config['SPOONACULAR_API_KEY']

router = Router()

translator = Translator()

@router.message(Command("random_recipe"))
async def send_random_recipe(message: Message):
    url = f'https://api.spoonacular.com/recipes/random?number=1&apiKey={SPOONACULAR_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        recipe = data['recipes'][0]
        title = recipe['title']
        summary = html2text.html2text(recipe['summary'])
        instructions = html2text.html2text(recipe['instructions'])

        # Перевод текста на русский язык
        title_ru = translator.translate(title, dest='ru').text
        summary_ru = translator.translate(summary, dest='ru').text
        instructions_ru = translator.translate(instructions, dest='ru').text

        recipe_details = f"Название: {title_ru}\n\nСуммарное описание: {summary_ru}\n\nИнструкции: {instructions_ru}"
        await message.reply(recipe_details)
    else:
        await message.reply("Не удалось получить рецепт. Попробуйте позже.")
