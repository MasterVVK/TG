import aiohttp
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import json

router = Router()

def load_config():
    with open('config.json', 'r', encoding='utf-8') as config_file:
        return json.load(config_file)

async def get_cat_image():
    config = load_config()
    CAT_API_KEY = config['CAT_API_KEY']
    url = f'https://api.thecatapi.com/v1/images/search?api_key={CAT_API_KEY}&include_breeds=true'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

@router.message(Command("cat"))
async def send_cat_image(message: Message):
    data = await get_cat_image()
    if data:
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
