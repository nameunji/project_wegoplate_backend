import re
import jwt
import json
import bcrypt

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


