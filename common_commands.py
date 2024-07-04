import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

# Команда /help
@router.message(Command("help"))
async def send_help(message: Message):
    logging.info("Получена команда /help")
    await message.reply(
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить помощь\n"
        "/weather <город> - Получить прогноз погоды для указанного города\n"
        "/voice - Записать и отправить голосовое сообщение\n"
        "/register - Зарегистрировать нового студента\n"
        "Просто отправьте текстовое сообщение, чтобы перевести его на английский язык.\n"
        "Отправьте фотографию, чтобы сохранить ее на сервере."
    )

# Обработчик текста "что такое ИИ?"
@router.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer(
        'Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ'
    )
