import bcrypt
import jwt
import re
import json

from django.views import View
from django.http  import JsonResponse

from my_settings  import SECRET,ALGORITHM
from .models      import User,Like
from .utils       import token_check
from company.models import Company

class DuplicationView(View):
    def post(self , request):
        try:
            data    = json.loads(request.body)
            email   = data ["email"]
            pattern = r'[A-Z0-9._%+-]+@[A-Z0-9,-]+\.[A-Z]{2,4}'    
            regex   = re.compile(pattern,flags=re.IGNORECASE)
            users   = User.objects.filter(email=email)

            if len(regex.findall(email)) == 0:
                return JsonResponse({"message":"EMAIL_INVALID"},status=400)
            
            if users:
                return JsonResponse({"message":"SIGN_IN"},status=200)
            
            return JsonResponse({"message":"SIGN_UP"},status=200)

        except KeyError:
            return JsonResponse({"message":"Key_Error"},status=400)

class SignUpView(View):
    def post(self , request):
        try :
            data          = json.loads(request.body)
            email         = data ["email"]
            password      = data ["password"]
            name          = data ["name"]
            phone         = data ["phone"]
            phoneRegex    = re.compile(r'(\d{2,3}-\d{3,4}-\d{4})', re.VERBOSE)  
            hash_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            
            if phoneRegex.findall(phone):  
                pass
            else :
                phone='null'

            User.objects.create(
                email    = email,
                password = hash_password,
                name     = name ,
                phone    = phone 
            )
            return JsonResponse({"message":"SUCCESS"},status=201)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)

class SignInView(View):
    def post(self , request):
        try : 
            data     = json.loads(request.body)
            email    = data["email"]
            password = data["password"]
            get_pw   = User.objects.get(email=email).password.encode('utf-8')
            users    = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), get_pw) :
                access_token    = jwt.encode({'user_id' : users.id}, SECRET, algorithm = ALGORITHM).decode('utf-8')
                return JsonResponse ({"message":"SUCCESS",'authorization':access_token },status=200)

            return JsonResponse({"message":"INVALID EMAIL OR PASSWORD"},status=400)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
            
class LikeView(View):
    @token_check
    def post(self , request):
        try:
            data            = json.loads(request.body)
            company_id      = data["company_id"]
            user_id         = request.user.id   
            get_user_id     = User.objects.get(id=user_id).id
            get_company_id  = Company.objects.get(id=company_id).id
            
            if get_user_id and get_company_id :
                Like.objects.create(user_id = get_user_id , company_id=get_company_id)
                return JsonResponse({"message":"SUCCESS"},status=201)
            
            return JsonResponse({"message":"user_id or company_id INVALID"},status=400)
        
        except Company.DoesNotExist:
            return JsonResponse({"message":"user_id or company_id INVALID"},status=400)

    @token_check
    def get(self , request):
        user_id = request.user.id 
        
        company_list=[
                { 
                "id"            :like_related.id , 
                "title"         :like_related.title ,
                "name"          :like_related.name,
                "city"          :like_related.district.city.name,   
                "compensation"  :like_related.compensation.recommender+like_related.compensation.applicant,
                "like_count"    :like_related.likes_count,
                "response_rate" :like_related.response_rate.rate,
                "image_url"     :like_related.image_url   
            } for like_related in  User.objects.get(id=user_id).likes.select_related('district__city', 'compensation', 'response_rate')]

        return JsonResponse( {"message":"SUCCESS","job_list":company_list},status=201)