import jwt
<<<<<<< HEAD
=======

>>>>>>> 20dac69... Add : 탐색페이지(카테고리,필터리스트,회사공고 리스트,회사공고 상세페이지,회사 리스트 필터링)
from django.http import JsonResponse
from .models import User
from my_settings  import SECRET,ALGORITHM
def token_check(func): 
    def wrapper(self, request, *args, **kwargs):
<<<<<<< HEAD
        encode_token = request.headers.get('AUTHORIZATION', None)
        if encode_token == None: 
            return func(self, request, *args, **kwargs)
=======

        encode_token = request.headers.get('AUTHORIZATION', None)

        if encode_token == None: 
            return func(self, request, *args, **kwargs)

>>>>>>> 20dac69... Add : 탐색페이지(카테고리,필터리스트,회사공고 리스트,회사공고 상세페이지,회사 리스트 필터링)
        try:
            payload  = jwt.decode(encode_token, SECRET, algorithm = ALGORITHM)                         
            user     = User.objects.get(id=payload["user_id"])
            if user == None :
                return JsonResponse({"message":"INVALID_USER"}, status=400)
            request.user = user
            return func(self, request,*args ,**kwargs) 
            
        except jwt.DecodeError:
            return JsonResponse({"message":"INVALID_TOKEN"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message":"UNKNOWN_USER"}, status=400)
    return wrapper