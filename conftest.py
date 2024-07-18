import pytest
import json
from unittest.mock import patch, mock_open

@pytest.fixture(autouse=True)
def mock_config():
    mock_config_data = {
        "CAT_API_KEY": "test_api_key"
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_config_data))):
        yield
