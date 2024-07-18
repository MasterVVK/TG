import pytest
from aioresponses import aioresponses
from cat_api_handler import get_cat_image

@pytest.mark.asyncio
async def test_get_cat_image_success():
    with aioresponses() as m:
        url = 'https://api.thecatapi.com/v1/images/search?api_key=test_api_key&include_breeds=true'
        m.get(url, payload=[{'url': 'https://example.com/cat.jpg', 'breeds': [{'name': 'BreedName', 'description': 'BreedDescription'}]}])

        result = await get_cat_image()
        assert result == [{'url': 'https://example.com/cat.jpg', 'breeds': [{'name': 'BreedName', 'description': 'BreedDescription'}]}]

@pytest.mark.asyncio
async def test_get_cat_image_failure():
    with aioresponses() as m:
        url = 'https://api.thecatapi.com/v1/images/search?api_key=test_api_key&include_breeds=true'
        m.get(url, status=404)

        result = await get_cat_image()
        assert result is None
