from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get_submitData_id():
    response = client.get("/submitData/1", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "message": "Объект получен",
        "id": {
            "coords_id": {
                "id": 1,
                "longitude": 0,
                "height": 0,
                "latitude": 0
            },
            "id": 1,
            "date_added": "2022-02-21T14:14:00.720184",
            "beauty_title": "string",
            "other_titles": "string",
            "winter": "st",
            "summer": "st",
            "spring": "st",
            "user_id": {
                "email": "user@email.tld",
                "name": "Василий",
                "phone": "79031234567",
                "id": 1,
                "fam": "Пупкин",
                "otc": "Иванович"
            },
            "add_time": "2021-09-22T13:18:13.720184",
            "status": "new",
            "title": "string",
            "connect": ", ",
            "autumn": "st"
        }
    }

