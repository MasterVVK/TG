import pytest
from cat_api_handler import get_cat_image

@pytest.mark.asyncio
async def test_get_cat_image_success(mocker):
    # Мокирование успешного ответа
    mock_response = mocker.AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = [{'url': 'https://example.com/cat.jpg', 'breeds': [{'name': 'BreedName', 'description': 'BreedDescription'}]}]

    # Создание mock-объекта для ClientSession с поддержкой асинхронного контекстного менеджера
    mock_session = mocker.AsyncMock()
    mock_session.get.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    result = await get_cat_image()
    assert result == [{'url': 'https://example.com/cat.jpg', 'breeds': [{'name': 'BreedName', 'description': 'BreedDescription'}]}]

@pytest.mark.asyncio
async def test_get_cat_image_failure(mocker):
    # Мокирование неуспешного ответа
    mock_response = mocker.AsyncMock()
    mock_response.status = 404

    # Создание mock-объекта для ClientSession с поддержкой асинхронного контекстного менеджера
    mock_session = mocker.AsyncMock()
    mock_session.get.return_value.__aenter__.return_value = mock_response
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    result = await get_cat_image()
    assert result is None
