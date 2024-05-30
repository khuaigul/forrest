# # tests/test_routes.py
# import pytest
# from app import app
# from conftest import TestConfig
# from app import db
# from models import User


# from app.server.profile import getUserUsername

# @pytest.fixture(scope="module")
# def client():
#     app.config.from_object(TestConfig)
#     with app.test_client() as client:
#         yield client

# def test_upload(client):
    
#     user = User(email="user", password="1234")
#     db.session.add(user)
#     db.session.commit()
#     db.session.close()
#     name = getUserUsername(1)
#     print("NAME", name)
#     assert (name == "user")


# def test_upload2(client):
#     db.create_all()
#     user = User(email="user1", password="1234")
#     db.session.add(user)
#     db.session.commit()
#     db.session.close()
#     name = getUserUsername(1)
#     print("NAME", name)
#     assert (name == "user1")

