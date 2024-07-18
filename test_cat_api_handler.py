import pytest
from aioresponses import aioresponses
from cat_api_handler import get_cat_image, send_cat_image
from aiogram.types import Message
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_send_cat_image_success(mocker):
    mock_data = [{'url': 'https://example.com/cat.jpg', 'breeds': [{'name': 'BreedName', 'description': 'BreedDescription'}]}]
    mock_get_cat_image = mocker.patch('cat_api_handler.get_cat_image', return_value=mock_data)

    mock_message = AsyncMock(spec=Message)
    mock_message.reply_photo = AsyncMock()

    await send_cat_image(mock_message)

    mock_get_cat_image.assert_called_once()
    mock_message.reply_photo.assert_called_once_with(photo='https://example.com/cat.jpg', caption='Порода: BreedName\n\nОписание: BreedDescription')

@pytest.mark.asyncio
async def test_send_cat_image_failure(mocker):
    mock_get_cat_image = mocker.patch('cat_api_handler.get_cat_image', return_value=None)

    mock_message = AsyncMock(spec=Message)
    mock_message.reply = AsyncMock()

    await send_cat_image(mock_message)

    mock_get_cat_image.assert_called_once()
    mock_message.reply.assert_called_once_with("Не удалось получить изображение кота. Попробуйте позже.")
