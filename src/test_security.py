import requests

BASE_URL = "http://127.0.0.1:8000"

def test_idor():
    r = requests.get(f"{BASE_URL}/files/2", params={"user_id": 1})
    assert r.status_code == 404

def test_access():
    r = requests.get(f"{BASE_URL}/files/1", params={"user_id": 1})
    assert r.status_code == 200

def test_admin_delete():
    r = requests.delete(f"{BASE_URL}/files/2", params={"user_id": 3})
    assert r.status_code == 200

    r2 = requests.get(f"{BASE_URL}/files/2", params={"user_id": 3})
    assert r2.status_code == 404

if __name__ == "__main__":
    test_idor()
    test_access()
    test_admin_delete()
    print("All tests passed ✅")