import structlog
from structlog.testing import capture_logs
import json

def test_request_id_auto_generated(test_app):
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})

  assert "X-Request-ID" in response.headers
  assert len(response.headers["X-Request-ID"]) == 36
  assert len(response.headers["X-Request-ID"].split("-")[0]) == 8
  assert len(response.headers["X-Request-ID"].split("-")[1]) == 4
  assert len(response.headers["X-Request-ID"].split("-")[2]) == 4
  assert len(response.headers["X-Request-ID"].split("-")[3]) == 4
  assert len(response.headers["X-Request-ID"].split("-")[4]) == 12

def test_request_id_honored(test_app):
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"}, headers={"X-Request-ID": "test-request-id-123"})
  assert response.headers["X-Request-ID"] == "test-request-id-123"

def test_user_registered_event_logged_with_response_header_set(test_app):
  with capture_logs() as captured: 
    response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  
  assert any(c.get("event") == "user_registered" for c in captured)
  assert "X-Request-ID" in response.headers

def test_json_renderer_produces_valid_json():
  renderer = structlog.processors.JSONRenderer()
  result = renderer(None, "info", {"event": "test_event", "key": "value"})

  assert json.loads(result)
  assert json.loads(result)["event"] == "test_event"
