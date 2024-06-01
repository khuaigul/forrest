# # tests/test_routes.py
# import pytest
# from app import app
# from conftest import TestConfig
# from app import db
from models import User
# from app import db
# from app import app
from app.server.profile import getUserIDByUserView, getUserEmailByUserView
from app.viewModels import *
import unittest
from app.algorithms.recommendations import findKeyWords

class TestAlgorithm(unittest.TestCase):

    def test_key_words(self):
        str = "Посёлок городского ТИпа Шуя"
        keyWords = findKeyWords(str)
        self.assertEqual(keyWords, set(['Посёлок', 'ТИпа', 'Шуя']))

class TestProfile(unittest.TestCase):
    
    def test_get_userID_by_user_view(self):
        user = User(id=2, email="user1", password="123456789")
        id = getUserIDByUserView(UserView(user))
        self.assertEqual(id, 2)
    
    def test_get_email_by_user_view(self):
        user = User(id=2, email="user1", password="123456789")
        name = getUserEmailByUserView(UserView(user))
        self.assertEqual(name, "user1")



if __name__ == '__main__':
    unittest.main()


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

