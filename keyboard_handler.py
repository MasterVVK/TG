import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

router = Router()

# Создание клавиатуры с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Привет"),
            KeyboardButton(text="Пока")
        ]
    ],
    resize_keyboard=True
)

# Обработчик кнопки "Привет"
@router.message(F.text == "Привет")
async def handle_hello(message: Message):
    logging.info("Нажата кнопка Привет")
    await message.reply(f"Привет, {message.from_user.first_name}!")

# Обработчик кнопки "Пока"
@router.message(F.text == "Пока")
async def handle_goodbye(message: Message):
    logging.info("Нажата кнопка Пока")
    await message.reply(f"До свидания, {message.from_user.first_name}!")

# Команда /links для отображения инлайн-кнопок с URL-ссылками
@router.message(Command("links"))
async def send_links(message: Message):
    logging.info("Получена команда /links")
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://news.yandex.ru")],
        [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru")],
        [InlineKeyboardButton(text="Видео", url="https://youtube.com")]
    ])
    await message.reply("Выберите ссылку:", reply_markup=inline_keyboard)

# Команда /dynamic для отображения динамической инлайн-кнопки
@router.message(Command("dynamic"))
async def send_dynamic_keyboard(message: Message):
    logging.info("Получена команда /dynamic")
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ])
    await message.reply("Нажмите на кнопку:", reply_markup=inline_keyboard)

# Обработчик нажатия на кнопку "Показать больше"
@router.callback_query(lambda c: c.data == "show_more")
async def handle_show_more(callback_query: CallbackQuery):
    logging.info("Нажата кнопка Показать больше")
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
    ])
    await callback_query.message.edit_reply_markup(reply_markup=inline_keyboard)

# Обработчики нажатий на кнопки "Опция 1" и "Опция 2"
@router.callback_query(lambda c: c.data == "option_1")
async def handle_option_1(callback_query: CallbackQuery):
    logging.info("Нажата кнопка Опция 1")
    await callback_query.message.answer("Вы выбрали Опцию 1")

@router.callback_query(lambda c: c.data == "option_2")
async def handle_option_2(callback_query: CallbackQuery):
    logging.info("Нажата кнопка Опция 2")
    await callback_query.message.answer("Вы выбрали Опцию 2")
