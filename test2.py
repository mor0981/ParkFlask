import unittest
import pyrebase
import App
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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



db = firestore.client()

firebase = pyrebase.initialize_app(config)
auth= firebase.auth()

class TestHello(unittest.TestCase):
    #User login with correct details
    def test_correct(self):
        try:
            auth.sign_in_with_email_and_password("mor0981@gmail.com","12661266")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    #User login with uncorrect details
    def test_uncorrect(self):
        try:
            auth.sign_in_with_email_and_password("mor081@gmail.com","12661266")
            self.assertTrue(False)
        except:
            self.assertTrue(True)
    #Register User with correct details
    def test_register(self):
        try:
    
            email="newRr@gmail.com"
            password="123"
            username="new"
            #user=auth.create_user_with_email_and_password("newRr@gmail.com","123321")
            data={"username":username,"email":email,"password":password,"admin":False}
            #info=auth.get_account_info(user['idToken'])['users'][0]['localId']
            db.collection(u'Users').document().set(data)
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    #Register User with uncorrect details
    def test_register_uncorrect(self):
        try:
    
            email="r@gmail.com"
            password="12345"
            username="r"
            #user=auth.create_user_with_email_and_password("newRr@gmail.com","123321")
            data={"username":username,"email":email,"password":password,"admin":False}
            #info=auth.get_account_info(user['idToken'])['users'][0]['localId']
            db.collection(u'Users').document().set(data)
            self.assertTrue(False)
        except:
            self.assertTrue(True)
            
                


      
    # Delete exist user
    def test_delete_register(self):
        try:
            email="newRr@gmail.com"
            password="123"
            username="new"
            docs=db.collection(u'Users').stream()
            for doc in docs:
                d=doc.to_dict()
                if email==d['email'] and password==d['password']:
                    db.collection(u'Users').document(doc.id).delete()
                    return self.assertTrue(True)
        except:
            self.assertTrue(False)


    # Delete unexist user
    def test_delete_unexist_register(self):
        try:
            email="newRr@gmail.com"
            password="123"
            username="new"
            docs=db.collection(u'Users').stream()
            for doc in docs:
                d=doc.to_dict()
                if email==d['email'] and password==d['password']:
                    db.collection(u'Users').document(doc.id).delete()
                    return self.assertTrue(False)
        except:
            self.assertTrue(True)


    
    #Add new vaild park
    def test_add_park(self):
        data = {
        "name": "newTestPark",
        "other": "bialik",
        "shadowing": "Yes"
        }
        docs = db.collection(u'Parks').stream()
        canMakePark = True
        for doc in docs:
            dici = doc.to_dict()
            if data["name"] == dici['name'] and data["other"] == dici['other']:
                canMakePark = False

        if canMakePark:
            db.collection(u'Parks').document().set(data)
            self.assertTrue(True)
        else:
            self.assertTrue(False)
    


    #Add  exist park
    def test_add_unvaild_park(self):
        data = {
        "name": "פארק הסופרים",
        "other": "הודה הלוי",
        "shadowing": "no"
        }
        docs = db.collection(u'Parks').stream()
        canMakePark = True
        for doc in docs:
            dici = doc.to_dict()
            if data["name"] == dici['name'] and data["other"] == dici['other']:
                canMakePark = False

        if canMakePark:
            db.collection(u'Parks').document().set(data)
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    
    #Delete exist park
    def test_delete_park(self):
        try:
            parkName = "newTestPark"
            parkAddress = "bialik"

            docs = db.collection(u'Parks').stream()
            for doc in docs:
                dici = doc.to_dict()
                if parkName == dici['name'] and parkAddress == dici['other']:
                    print (f"park {dici['name']} in {dici['other']} has beem deleted")
                    db.collection(u'Parks').document(doc.id).delete()
                    
                    #print(db.collection(u'Parks').document(doc.id).delete())
                    self.assertTrue(True)
        except:
            self.assertTrue(False)

    #Delete unexist park
    def test_delete_unexist_park(self):
        try:
            parkName = "notFound"
            parkAddress = "never"

            docs = db.collection(u'Parks').stream()
            for doc in docs:
                dici = doc.to_dict()
                if parkName == dici['name'] and parkAddress == dici['other']:
                    #print (f"park {dici['name']} in {dici['other']} has beem deleted")
                    db.collection(u'Parks').document(doc.id).delete()
                    
                    #print(db.collection(u'Parks').document(doc.id).delete())
                    self.assertTrue(False)
        except:
            self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()
    
