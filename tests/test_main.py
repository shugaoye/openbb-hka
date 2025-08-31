import json
import pytest
from pathlib import Path
from fastapi.responses import JSONResponse
from main import get_apps

def test_get_apps(tmp_path):
    # Create a mock apps.json file
    mock_apps = {
        "app1": {"name": "Test App 1"},
        "app2": {"name": "Test App 2"}
    }
    apps_json = tmp_path / "apps.json"
    apps_json.write_text(json.dumps(mock_apps))
    
    # Mock Path(__file__).parent to return tmp_path
    def mock_path(monkeypatch):
        monkeypatch.setattr(Path, "parent", lambda _: tmp_path)
    
    # Call the function and verify response
    response = get_apps()
    assert isinstance(response, JSONResponse)
    assert response.status_code == 200
    #assert response.body == json.dumps(mock_apps).encode()