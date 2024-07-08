# random_recipe_handler.py

import requests
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("random_recipe"))
async def send_random_recipe(message: Message):
    url = 'https://api.randomrecipes.com/v1/random?number=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        recipe = data['recipes'][0]
        recipe_details = f"{recipe['title']}\n\n{recipe['summary']}\n\n{recipe['instructions']}"
        await message.reply(recipe_details)
    else:
        await message.reply("Не удалось получить рецепт. Попробуйте позже.")
