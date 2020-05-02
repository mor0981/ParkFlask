import unittest
import pyrebase
from App.py import app

config={
  "apiKey": "AIzaSyDab7tKKm11tgRuLsAPejXGGAYJ1d20cnQ",
  "authDomain": "parkflask.firebaseapp.com",
  "databaseURL": "https://parkflask.firebaseio.com",
  "projectId": "parkflask",
  "storageBucket": "parkflask.appspot.com",
  "messagingSenderId": "685599054335",
  "appId": "1:685599054335:web:db2d1d2890588a14772fca",
  "measurementId": "G-H8HGMEE4WB"
}

firebase = pyrebase.initialize_app(config)
auth= firebase.auth()

class TestHello(unittest.TestCase):
    #User login with correct details
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
    def test_correct(self):
        try:
            auth.sign_in_with_email_and_password("mor0981@gmail.com","12661266")
            self.assertTrue(True)
        except:
            self.assertTrue(False)
    #User login with incorrect details
    def test_incorrect(self):
        try:
            auth.sign_in_with_email_and_password("mor081@gmail.com","12661266")
            self.assertTrue(False)
        except:
            self.assertTrue(True)
    


if __name__ == '__main__':
    unittest.main()