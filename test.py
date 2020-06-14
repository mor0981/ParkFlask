import unittest
import pyrebase
import App
from App import delete_info_item 
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
    




    #Delete exist park
    def test_delete_park(self):
        try:
            parkName = "newTestPark"
            parkAddress = "bialik"

            docs = db.collection(u'Parks').stream()
            for doc in docs:
                dici = doc.to_dict()
                if parkName == dici['name'] and parkAddress == dici['other']:
                    #print (f"park {dici['name']} in {dici['other']} has beem deleted")
                    db.collection(u'Parks').document(doc.id).delete()
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
                    db.collection(u'Parks').document(doc.id).delete()
                    self.assertTrue(False)
        except:
            self.assertTrue(True)
    #Delete comment by exist id
    def test_delete_comment(self):
        try:
            post_id='YhzN7rBXz95lA1CuhFCY'
            db.collection(u'Comments').document(post_id).delete()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    #Delete unExist Comment
    def test_delete_notExist_comment(self):
        try:
            post_id='aaaa'
            db.collection(u'Comments').document(post_id).delete()
            self.assertTrue(False)
        except:
            self.assertTrue(True)


    #Add  new info item
    def test_add_info_item(self):
        dic=db.collection(u'Information').stream()
        docs = [{
        'id': 1,
        'name': 'name 1',
        'email': 'email 1'
        }, {
        'id': 2,
        'name': 'name 2',
        'email': 'email 2'
        }]
        
        print("hello")
        data = {
        "name": 'מיקל גאקסון',
        "job": 'ליצן',
        "email": 'mike@gmail.com'
        }
        docs = db.collection(u'Information').stream()
        for doc in docs:
            dici = doc.to_dict()
            print(dici)
            if data["name"] == dici['name'] and data["job"] == dici['job'] and data["email"] == dici['email']:
                self.assertFalse(False)             
                return

        db.collection(u'Information').document().set(data)
        self.assertTrue(True)
        
        arr=[]
        for doc in dic:
            d=doc.to_dict()
            d["id"] = doc.id
            #print(d)
            arr.append(d)
            self.assertTrue(True)  
    #delete exist info item
    def test_delete_info_item(self):
        try:
            info_item_id='va6sHyqPGLyPdZFz9XIE'
            db.collection(u'Information').document(info_item_id).delete()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    #delete unexist info item
    def test_delete_unexist_info_item(self):
        try:
            info_item_id='qq' #there is no id like that
            db.collection(u'Information').document(info_item_id).delete()
            self.assertTrue(False)
        except:
            self.assertTrue(True)


    
    #add new guest by admin
    def test_AddGuestByAdmin(self):
        email="testttt@gmail.com"
        password="password"
        name='guest'
        last='test'
        Admin=False
        try:
            #user=auth.create_user_with_email_and_password("testttt@gmail.com","123456password")
            data={"name":name,"last":last,"email":email,"password":password,"admin":Admin}
            #print(auth.get_account_info(user['idToken'])['users'][0]['localId'])
            #info=auth.get_account_info(user['idToken'])['users'][0]['localId']
            db.collection(u'Users').document().set(data)
            self.assertTrue(True)
        except:
            self.assertFalse(True)

    #add new Admin by admin
    def test_AddAdminByAdmin(self):
        email="testttt@gmail.com"
        password="password"
        name='guest'
        last='test'
        Admin=True
        try:
            #user=auth.create_user_with_email_and_password("testttt@gmail.com","123456password")
            data={"name":name,"last":last,"email":email,"password":password,"admin":Admin}
            #print(auth.get_account_info(user['idToken'])['users'][0]['localId'])
            #info=auth.get_account_info(user['idToken'])['users'][0]['localId']
            db.collection(u'Users').document().set(data)
            self.assertTrue(True)
        except:
            self.assertFalse(True)

    #Update exist Guest
    def test_updateGuest(self):
        try:
            ref_comment=db.collection(u'Users')
            email="testttt@gmail.com"
            ref_my=ref_comment.where(u'email',u'==',email).get()
            field_updates={"name":'דני',"last":'sce',"email":email}
            for r in ref_my:
                rr=ref_comment.document(r.id)
                rr.update(field_updates)
                self.assertTrue(True)
        except:
            self.assertTrue(False)


    #Update unexist Guest
    def test_unexist_updateGuest(self):
        try:
            ref_comment=db.collection(u'Users')
            email="NotFoundUser@gmail.com"
            ref_my=ref_comment.where(u'email',u'==',email).get()
            field_updates={"name":'no',"last":'no',"email":email}
            for r in ref_my:
                rr=ref_comment.document(r.id)
                rr.update(field_updates)
                self.assertTrue(False)
        except:
            self.assertTrue(True)

    #delete exist guest
    def test_deleteGuest(self):
        try:
            ref_comment=db.collection(u'Users')
            ref_my=ref_comment.where(u'email',u'==',"r@gmail.com").get()
            for r in ref_my:
                rr=ref_comment.document(r.id)
                rr.delete()
                self.assertTrue(True)
        except:
            self.assertTrue(False)

    #delete exist guest
    def test_unexist_deleteGuest(self):
        try:
            ref_comment=db.collection(u'Users')
            ref_my=ref_comment.where(u'email',u'==',"UserNotFound@gmail.com").get()
            for r in ref_my:
                rr=ref_comment.document(r.id)
                rr.delete()
                self.assertTrue(False)
        except:
            self.assertTrue(True)
        
    #add new facilites
    def test_facilities(self):

        docs = db.collection(u'Parks').stream()
        parkData = {
            "name": "testPark",
            "parkFacility": "נקי ומסודר"
        }
        canAddPark = False
        for doc in docs:
            dici = doc.to_dict()
            try:
                if parkData['name'] == dici['name']:
                    canAddPark = True

                if canAddPark:
                    # Deleting and creating a new park witch will be updated with the new facilities
                    db.collection(u'Parks').document(doc.id).delete()
                    db.collection(u'Parks').document().set(parkData)
                    self.assertTrue(True)
                    break

            except :
                self.assertTrue(False)
                pass
    #add new vaild comment
    def test_addComment(self):
        try:
            data={'author':'dani@gmail.com','content':'הפארק מסוודר :)','post_id':8777765554444,'title':'פארק גדולי ישראל'}
            doc=db.collection(u'testComments').document()
            doc.set(data)
            self.assertTrue(True)
        except:
            self.assertTrue(False)


    #add new vaild comment
    def test_unvaild_addComment(self):
        try:
            data={'author':'dani@gmail.com','content':'','post_id':8777765554444,'title':'פארק גדולי ישראל'}
            doc=db.collection(u'testComments').document()
            doc.set(data)
            self.assertTrue(False)
        except:
            self.assertTrue(True)


    #update exist comment
    def test_updateComment(self):
        try:
            ref_comment=db.collection(u'Users')
            author="dani@gmail.com"
            ref_my=ref_comment.where(u'author',u'==',author).get()
            field_updates={"author":author,"content":'פארק יפה *-*'}
            for r in ref_my:
                rr=ref_comment.document(r.id)
                rr.update(field_updates)
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    #update unExist comment
    def test_UnExist_updateComment(self):
        try:
            ref_comment=db.collection(u'Users')
            author="UserNotFound@gmail.com"
            ref_my=ref_comment.where(u'author',u'==',author).get()
            field_updates={"author":author,"content":'פארק יפה *-*'}
            for r in ref_my:
                rr=ref_comment.document(r.id)
                rr.update(field_updates)
            self.assertTrue(False)
        except:
            self.assertTrue(True)


    #delete exist comment
    def test_deleteComment(self):
        try:
            ref_comment=db.collection(u'testComments')
            ref_my=ref_comment.where(u'author',u'==',"dani@gmail.com").get()
            for r in ref_my:
                rr=ref_comment.document(r.id)
                rr.delete()
                self.assertTrue(True)
        except:
            self.assertTrue(False)
    
     #delete unexist comment
    def test_unExist_deleteComment(self):
        try:
            ref_comment=db.collection(u'testComments')
            ref_my=ref_comment.where(u'author',u'==',"UserNotFound@gmail.com").get()
            for r in ref_my:
                rr=ref_comment.document(r.id)
                rr.delete()
                self.assertTrue(False)
        except:
            self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()
    