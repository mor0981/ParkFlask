import unittest
from App import app
import json 



class TestHello(unittest.TestCase):
    #User login with correct details
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_homePage(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')

    

    def test_login_logout(self):
        taster = app.test_client(self)
        rv = taster.post('/login' , data=dict(email="mor0981@gmail.com",password="123456"),follow_redirects=True)
        self.assertTrue(rv.status, '200 OK')
        self.assertTrue('ברוכים'.encode() in rv.data)
        rv= taster.get('/logout',follow_redirects=True)
        self.assertTrue('התנתקת בהצלחה'.encode() in rv.data)

    def test_login_session(self):
        taster = app.test_client(self)
        rv = taster.post('/login' , data=dict(email="mor0981@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.get('/login',follow_redirects=True)
        self.assertTrue('ברוכים'.encode() in rv.data)

    def test_delete_user(self):
        taster = app.test_client(self)
        rv = taster.post('/register' , data=dict(email="test@gmail.com",password="123456",name="test",last="test"),follow_redirects=True)
        rv = taster.post('/login' , data=dict(email="test@gmail.com",password="123456"),follow_redirects=True)
        self.assertTrue('ברוכים'.encode() in rv.data)
        rv = taster.post('/unregister' , data=dict(email="test@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.post('/login' , data=dict(email="test@gmail.com",password="123456"),follow_redirects=True)
        self.assertTrue('שם משתמש או סיסמא לא נכונים'.encode() in rv.data)

    def test_comment(self):
        taster = app.test_client(self)
        rv = taster.post('/register' , data=dict(email="test2@gmail.com",password="123456",name="test",last="test"),follow_redirects=True)
        rv = taster.post('/login' , data=dict(email="test2@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.post('/comments/פארק%20ליכטנשטיין',data=dict(comment="test"),follow_redirects=True)
        rv = taster.get('/comments/פארק%20ליכטנשטיין')
        self.assertTrue('test'.encode() in rv.data)
        rv = taster.post('/unregister',data=dict(email="test2@gmail.com",password="123456"),follow_redirects=True)

    def test_jasonPark_show(self):
        taster = app.test_client(self)
        with open('playgrounds.json', 'r',encoding="utf8") as myfile:
            arr=[]
            data=json.loads(myfile.read())
        arr.append(data[0]['Name'])
        rv = taster.post('/login' , data=dict(email="mor0981@gmail.com",password="123456"),follow_redirects=True)
        rv = taster.get('/parks')
        for p in arr:
            self.assertTrue(p.encode() in rv.data)

    
        

         
        
    # def test_correct(self):
    #     try:
    #         auth.sign_in_with_email_and_password("mor0981@gmail.com","123456")
    #         self.assertTrue(True)
    #     except:
    #         self.assertTrue(False)
    # #User login with incorrect details
    
    # def test_incorrect(self):
    #     try:
    #         auth.sign_in_with_email_and_password("mor081@gmail.com","12661266")
    #         self.assertTrue(False)
    #     except:
    #         self.assertTrue(True)
    


if __name__ == '__main__':
    unittest.main()