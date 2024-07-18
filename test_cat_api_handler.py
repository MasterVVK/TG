import pytest
from unittest.mock import AsyncMock
from cat_api_handler import get_cat_image, send_cat_image
from aiogram.types import Message

API_URL = "https://api.thecatapi.com/v1/images/search?api_key=test_api_key&include_breeds=true"

@pytest.mark.asyncio
async def test_get_cat_image_success(mocker):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = [{"url": "https://example.com/cat.jpg", "breeds": [{"name": "BreedName", "description": "BreedDescription"}]}]

    mock_get = mocker.patch('aiohttp.ClientSession.get', return_value=mock_response)
    result = await get_cat_image()
    mock_get.assert_called_once_with(API_URL)
    assert result == [{"url": "https://example.com/cat.jpg", "breeds": [{"name": "BreedName", "description": "BreedDescription"}]}]

@pytest.mark.asyncio
async def test_get_cat_image_failure(mocker):
    mock_response = AsyncMock()
    mock_response.status = 404

    mock_get = mocker.patch('aiohttp.ClientSession.get', return_value=mock_response)
    result = await get_cat_image()
    mock_get.assert_called_once_with(API_URL)
    assert result is None

@pytest.mark.asyncio
async def test_send_cat_image_success(mocker):
    mock_data = [{"url": "https://example.com/cat.jpg", "breeds": [{"name": "BreedName", "description": "BreedDescription"}]}]
    mocker.patch('cat_api_handler.get_cat_image', return_value=mock_data)

    mock_message = mocker.AsyncMock(spec=Message)
    mock_message.reply_photo = mocker.AsyncMock()

    await send_cat_image(mock_message)

    mock_message.reply_photo.assert_called_once_with(photo="https://example.com/cat.jpg", caption="Порода: BreedName\n\nОписание: BreedDescription")

@pytest.mark.asyncio
async def test_send_cat_image_failure(mocker):
    mocker.patch('cat_api_handler.get_cat_image', return_value=None)

    mock_message = mocker.AsyncMock(spec=Message)
    mock_message.reply = mocker.AsyncMock()

    await send_cat_image(mock_message)

    mock_message.reply.assert_called_once_with("Не удалось получить изображение кота. Попробуйте позже.")
