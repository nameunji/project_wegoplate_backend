import re
import jwt
import json
import bcrypt

from django.views               import View
from django.http                import JsonResponse
from django.db                  import IntegrityError
from django.core.validators     import validate_email
from django.core.exceptions     import ValidationError

from user.models                import User
from WegoPlate_backend.settings import SECRET_KEY
from unittest.mock              import patch, MagicMock

from django.test                import TestCase
from django.test                import Client



class UserTest(TestCase):
    def setUp(self):
        client = Client()
        User.objects.create(
            nick_name = 'wecode',
            email     = 'wecode@gmail.com',
            password  = bcrypt.hashpw('wecode1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def test_possible_nickname(self):
        client = Client()
        test = {'nick_name':'test'}
        response = client.post('/user/nickname', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message':'POSSIBLE'})

    def test_duplication_nickname(self):
        client = Client()
        test = {'nick_name':'wecode'}
        response = client.post('/user/nickname', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'DUPLICATION_NICKNAME'})


    def test_signup_check(self):
        client = Client()
        test = {
            'nick_name' : 'test',
            'email'     : 'test@gmail.com',
            'password'  : 'test1234'
        }
        response = client.post('/user', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_signup_email_check(self):
        client = Client()
        test = {
            'nick_name' : 'test1',
            'email'     : 'test1gmail.com',
            'password'  : 'test1234'
        }
        response = client.post('/user', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_EMAIL'})
    
    def test_signup_nickname_check(self):
        client = Client()
        test = {
            'nick_name' : 't',
            'email'     : 'test1@gmail.com',
            'password'  : 'test1234'
        }
        response = client.post('/user', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'NICKNAME_SHORT'})

    def test_signup_password_check(self):
        client = Client()
        test = {
            'nick_name' : 'test1',
            'email'     : 'test1@gmail.com',
            'password'  : 'test'
        }
        response = client.post('/user', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_PASSWORD'})

    def test_signup_invalide_key_check(self):
        client = Client()
        test = {
            'nick_name' : 'test1',
            'email'     : 'test1@gmail.com'
        }
        response = client.post('/user', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_KEYS'})

    def test_signin_check(self):
        client = Client()
        test = {
            'email'     : 'wecode@gmail.com',
            'password'  : 'wecode1234'
        }
        response = client.post('/user/signin', json.dumps(test), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_signin_invalid_key_check(self):
        client = Client()
        test = {
             'email' : 'wecode@gmail.com',
        }
        response = client.post('/user/signin', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_KEYS'})

    def test_signin_invalid_user_check(self):
        client = Client()
        test = {
            'email' : 'test1@gmail.com',
            'password' : 'test'
        }
        response = client.post('/user/signin', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_USER'})
        
    @patch('user.views.requests')
    def test_kakao_signin(self,mocked_requests):
        client = Client()
        mock_dict = {
            'id' : '1234', 
            'properties' : {'nickname' : 'jj'}
            }

        class MockedResponse:
            def json(self):
                return mock_dict

        mocked_requests.get = MagicMock(return_value = MockedResponse())

        test = {
            'kakao' : '1234',
            'email' : 'test@gmail.com',
            'password' : '1234'
        }

        header = {'HTTP_Authorization' : '1234ABCD'}
        response = client.post('/user/kakao', content_type='applications/json', **header)

        self.assertEqual(response.status_code, 200)
        
    def tearDown(self):
        User.objects.all().delete()

    
    


