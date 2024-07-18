# test_cat_api_handler.py

import pytest
from aioresponses import aioresponses
from cat_api_handler import get_cat_image, send_cat_image
from aiogram.types import Message
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_get_cat_image_success():
    with aioresponses() as m:
        url = 'https://api.thecatapi.com/v1/images/search'
        params = {'api_key': 'test_api_key', 'include_breeds': 'true'}
        m.get(url, payload=[{'url': 'https://example.com/cat.jpg', 'breeds': [{'name': 'BreedName', 'description': 'BreedDescription'}]}], params=params)

        result = await get_cat_image()
        assert result == [{'url': 'https://example.com/cat.jpg', 'breeds': [{'name': 'BreedName', 'description': 'BreedDescription'}]}]

@pytest.mark.asyncio
async def test_get_cat_image_failure():
    with aioresponses() as m:
        url = 'https://api.thecatapi.com/v1/images/search'
        params = {'api_key': 'test_api_key', 'include_breeds': 'true'}
        m.get(url, status=404, params=params)

        result = await get_cat_image()
        assert result is None

@pytest.mark.asyncio
async def test_send_cat_image_success():
    mock_data = [{'url': 'https://example.com/cat.jpg', 'breeds': [{'name': 'BreedName', 'description': 'BreedDescription'}]}]

    async def mock_get_cat_image():
        return mock_data

    mock_message = MagicMock(spec=Message)
    mock_message.reply_photo = MagicMock()

    with patch('cat_api_handler.get_cat_image', new=mock_get_cat_image):
        await send_cat_image(mock_message)

    mock_message.reply_photo.assert_called_once_with(photo='https://example.com/cat.jpg', caption='Порода: BreedName\n\nОписание: BreedDescription')

@pytest.mark.asyncio
async def test_send_cat_image_failure():
    async def mock_get_cat_image():
        return None

    mock_message = MagicMock(spec=Message)
    mock_message.reply = MagicMock()

    with patch('cat_api_handler.get_cat_image', new=mock_get_cat_image):
        await send_cat_image(mock_message)

    mock_message.reply.assert_called_once_with("Не удалось получить изображение кота. Попробуйте позже.")
