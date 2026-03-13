import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: 無需特別準備，直接測試查詢活動
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_activity():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()

    # 再次報名同一活動，應該失敗
    response_repeat = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response_repeat.status_code != 200
    assert "detail" in response_repeat.json()

def test_unregister_activity():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    # Assert
    assert response.status_code == 200 or response.status_code == 404
    # 若已取消報名，應回傳訊息或錯誤
    assert "message" in response.json() or "detail" in response.json()
