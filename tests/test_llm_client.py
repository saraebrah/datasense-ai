from unittest.mock import Mock, patch

from app.llm_client import LLMClient


def test_llm_client_configuration():
    client = LLMClient(
        base_url="http://test-server",
        model="test-model",
        timeout=15,
    )

    assert client.base_url == "http://test-server"
    assert client.model == "test-model"
    assert client.timeout == 15


@patch("app.llm_client.requests.post")
def test_generate_text(mock_post):

    mock_response = Mock()

    mock_response.json.return_value = {
        "message": {
            "content": "Test response"
        }
    }

    mock_post.return_value = mock_response

    client = LLMClient(
        base_url="http://test-server",
        model="test-model",
        timeout=15,
    )

    result = client.generate_text(
        "Test prompt"
    )

    assert result == "Test response"


    mock_post.assert_called_once_with(
        "http://test-server/api/chat",
        json={
            "model": "test-model",
            "messages": [
                {
                    "role": "user",
                    "content": "Test prompt",
                }
            ],
            "stream": False,
        },
        timeout=15,
    )


    mock_response.raise_for_status.assert_called_once()
    