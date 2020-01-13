import re
import jwt
import json
import bcrypt
import requests

from django.views               import View
from django.db                  import IntegrityError
from django.core.validators     import validate_email
from django.core.exceptions     import ValidationError
from django.http                import JsonResponse, HttpResponse

from .models                    import User
from WegoPlate_backend.settings import SECRET_KEY

class NicknameCheckView(View):
    def post(self, request):
        data = json.loads(request.body)

        check = User.objects.filter(nick_name = data["nick_name"])
        if check.exists():
            return JsonResponse({'message':'DUPLICATION_NICKNAME'}, status = 400)
        else:
            return JsonResponse({'message': 'POSSIBLE'}, status = 200)


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        check_password = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

        try:
            validate_email(data["email"])

            if len(data["nick_name"]) < 2 :
                return JsonResponse({'message':'NICKNAME_SHORT'}, status = 400)

            if not check_password.match(data["password"]):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status = 400)
            
            hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
            User(
                nick_name = data["nick_name"],
                email    = data["email"],
                password = hashed_password.decode('utf-8')
            ).save()
            return HttpResponse(status=200)

        except ValidationError:
            return JsonResponse({'message':'INVALID_EMAIL'}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email = data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm='HS256')

                return JsonResponse(
                    {
                        'access_token' : access_token.decode('utf-8'),
                        'message' : "POSSIBLE"
                    }, status=200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)
        
        except ValueError:
            return JsonResponse({'message' : 'INVALID_VALUE'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)

class SocialKakaoView(View):
    def post(self, request):

        kakao_token = request.headers["Authorization"]
        if not kakao_token:
            return JsonResponse({"MESSAGE" : "INVALID_KAKAO_TOKEN"}, status=400)

        headers = {'Authorization' : f"Bearer {kakao_token}"}
        url = "https://kapi.kakao.com/v2/user/me"
        response = requests.get(url, headers = headers)
        kakao_user = response.json()

        if User.objects.filter(kakao = kakao_user['id']).exists():

            user = User.objects.get(kakao = kakao_user['id'])
            access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm='HS256')

            return JsonResponse({'access_token' : access_token.decode('utf-8'),}, status=200)

        else :
            newUser = User.objects.create(
                kakao = kakao_user['id'],
                nick_name = kakao_user['properties']['nickname']
            )

            access_token = jwt.encode({'id' : newUser.id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'access_token': access_token.decode('utf-8')}, status=200)