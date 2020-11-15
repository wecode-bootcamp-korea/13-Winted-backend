import bcrypt
import jwt
import re
import json
import requests

from django.views import View
from django.http  import JsonResponse

from my_settings  import SECRET,ALGORITHM
from .models      import User,Like,AppliedStatus,UserTagFilter,UserDistrictFilter,UserCareerFilter
from .utils       import token_check
from company.models import Company,Tag,District

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
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

class SignUpView(View):
    def post(self , request):
        try :
            data          = json.loads(request.body)
            email         = data ["email"]
            password      = data ["password"]
            name          = data ["name"]
            phone         = data ["phone"] 
            hash_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
                email    = email,
                password = hash_password,
                name     = name ,
                phone    = phone,
                profile_image_url = 'https://us.123rf.com/450wm/thesomeday123/thesomeday1231712/thesomeday123171200009/91087331-%EB%82%A8%EC%84%B1%EC%9D%84%EC%9C%84%ED%95%9C-%EA%B8%B0%EB%B3%B8-%EC%95%84%EB%B0%94%ED%83%80-%ED%94%84%EB%A1%9C%ED%95%84-%EC%95%84%EC%9D%B4%EC%BD%98-%ED%9A%8C%EC%83%89-%EC%82%AC%EC%A7%84-%EC%9E%90%EB%A6%AC-%ED%91%9C%EC%8B%9C-%EC%9E%90-%EC%9D%BC%EB%9F%AC%EC%8A%A4%ED%8A%B8-%EB%B2%A1%ED%84%B0.jpg?ver=6'
            )
            return JsonResponse({"message":"SUCCESS"},status=201)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

class SignInView(View):
    def post(self , request):
        try : 
            data              = json.loads(request.body)
            email             = data["email"]
            password          = data["password"]
            password_encode   = User.objects.get(email=email).password.encode('utf-8')
            users             = User.objects.get(email=email)

            user_data = {
                'id'               : users.id,
                'email'            : users.email,
                'phone'            : users.phone,
                'name'             : users.name,
                'profile_image_url': users.profile_image_url
            }

            if bcrypt.checkpw(password.encode('utf-8'), password_encode) :
                access_token  = jwt.encode({'user_id' : users.id}, SECRET, algorithm = ALGORITHM).decode('utf-8')
                return JsonResponse ({"message":"SUCCESS",'authorization':access_token, 'user_data' : user_data },status=200)

            return JsonResponse({"message":"INVALID EMAIL OR PASSWORD"},status=400)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

class KakaoLoginView(View):
    def post(self, request):
        try:
            
            access_token    = request.headers.get('Authorization')
            profile_request = requests.get(                               
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},
            )
            
            profile_json  = profile_request.json()
            kakao_account = profile_json.get("kakao_account")
            email         = kakao_account.get("email", None)
            url           = profile_json['kakao_account']['profile']["profile_image_url"]
            name          = profile_json['kakao_account']['profile']["nickname"]
            kakao_id      = profile_json['id']
            users         = User.objects.filter(email=email)
            user_data     = {
                'id'               : kakao_id,
                'email'            : email,
                'name'             : name,
                'profile_image_url': url
            }
                
            if not users : 
                User.objects.create(
                    email=email,
                    password='',
                    phone = '',
                    name=name ,
                    profile_image_url=url
                )

            winted_token   = jwt.encode({'user_id' : users[0].id}, SECRET, algorithm = ALGORITHM).decode('utf-8')
            return JsonResponse({"message":"SUCCESS",'authorization':winted_token,'user_data' : user_data},status=201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR' }, status = 400)
        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)
  
class LikeView(View):
    @token_check
    def post(self , request):
        try:
            data         = json.loads(request.body)
            user_id      = request.user.id   
            company      = Company.objects.get(id=data['company_id'])
            likes        = Like.objects.filter (user_id = user_id , company_id=company.id)
            
            if user_id and company.id and not likes:
                Like.objects.create(user_id = user_id , company_id=company.id)
                company.likes_count += 1
                company.save()

                return JsonResponse({"message":"SUCCESS"},status=201)

            elif likes.exists():
                likes.delete()
                company.likes_count -= 1
                company.save()

                return JsonResponse({"message":"SUCCESS"},status=200)
        
        except Company.DoesNotExist:
            return JsonResponse({"message":"company_id INVALID"},status=400)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)

        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)

    @token_check
    def get(self , request):
        user_id = request.user.id 
        
        company_list=[
                { 
                "id"            :applied_status.id,
                "title"         :applied_status.title,
                "name"          :applied_status.name,
                "city"          :applied_status.district.city.name,   
                "compensation"  :applied_status.compensation.recommender+applied_status.compensation.applicant,
                "likes_count"   :applied_status.likes_count,
                "response_rate" :applied_status.response_rate.rate,
                "image_url"     :[image for image in applied_status.image_url.split(',')][0],
                "likes_status"  :True
            } for applied_status in  User.objects.get(id=user_id).likes.select_related('district__city', 'compensation', 'response_rate')]

        return JsonResponse( {"message":"SUCCESS","job_list":company_list},status=200)

class TagView(View):
   
    @token_check 
    def post(self , request):
        try :
            data     = json.loads(request.body) 
            user_id  = request.user.id   
        
            if  "tag_list" in data : 
                tag_list  = data["tag_list"]

                if  data.get('tag_list') :
                    UserTagFilter.objects.filter(user_id=user_id).delete()
                    for tag in tag_list:
                        UserTagFilter.objects.create(user_id=user_id, tag_id=tag)

            if  "district_list" in data :
                district_list = data ["district_list"]

                if  data.get('district_list') :
                    UserDistrictFilter.objects.filter(user_id=user_id).delete()
                    for district in district_list:
                        UserDistrictFilter.objects.create(user_id=user_id, district_id=district)

            if  "career_list" in data :
                career_list  = data ["career_list"] 

                UserCareerFilter.objects.filter(user_id=user_id).delete()
                for career in career_list:
                    UserCareerFilter.objects.create(user_id=user_id, career_id=career)

            return JsonResponse({"message":"SUCCESS"},status=200)

        except json.decoder.JSONDecodeError :
            return JsonResponse({"message":"Json_Decode_Error"},status=400)
        
    @token_check
    def get(self , request):
        user_id = request.user.id 
        
        tag=[
                { 
                "id"    :tags.id , 
                "name"  :tags.name 
            } for tags in  User.objects.get(id=user_id).tag_filters.select_related()]
            
        city=[
                {     
                "id"       :district.id , 
                "city"     :district.city.name,
                "district" :district.name           
            } for district in  User.objects.get(id=user_id).district_filters.select_related()]
        
        career=[
                {     
                "id"   :career.id , 
                "name" :career.name            
            } for career in  User.objects.get(id=user_id).career_filters.select_related()]
        
        return JsonResponse( {"message":"SUCCESS","tag":tag , "city" :city ,"career" :career},status=200)