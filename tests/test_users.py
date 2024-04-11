# # write test cases for the following:
# # 1. check if authentication works properly
# # 2. check if user creation works properly

# # Path: tests/test_users.py
# from fastapi.testclient import TestClient
# from app.main import app
# from app.core.authentication import hash_password
# from app.models.users import User
# from app.db.session import SessionLocal
# import json
# from app.schemas.user import UserCreate
# from app.core.authentication import create_access_token
# from app.core.config import settings
# from app.models.base import CRUDUser
# from app.core.authentication import check_password
# from sqlalchemy.exc import IntegrityError

# client = TestClient(app)
# crud_user = CRUDUser(User)

# def test_authenticate_user():
#     response = client.post("/api/v1/users/auth", data={"username": "chitharthan", "password": "password"})
#     assert response.status_code == 401
#     user = crud_user.get_by_email(SessionLocal(), email="chitharthan")
#     user.password = hash_password("password")
#     response = client.post("/api/v1/users/auth", data={"username": "chitharthan", "password": "password"})
#     assert response.status_code == 200
#     assert response.json()["access_token"]
#     assert response.json()["token_type"] == "bearer"
#     assert check_password("password", user.password)


# def test_create_user():
#     response = client.post("/api/v1/users/", json={"email": "chitharthan.s@gmail.com", "password": "password"})
#     assert response.status_code == 401
#     token = create_access_token(data={"sub": "chitharthan"})
#     response = client.post("/api/v1/users/", json={"email": "chitharthan.s@gmail.com", "password": "password"}, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     assert response.json()["email"] == "chitharthan.s@gmail.com"
#     response = client.post("/api/v1/users/", json={"email": "chitharthan.s@gmail.com", "password": "password"}, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Email already registered"
#     response = client.post("/api/v1/users/", json={"email": "chitharthan.s@gmail.com", "password": "password"}, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Email already registered integrity error"


def test_sample():
    assert 1 == 1