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

class SignUpView(View):
    def post(self , request):
        try :
            data          = json.loads(request.body)
            email         = data ["email"]
            password      = data ["password"]
            name          = data ["name"]
            phone         = data ["phone"]
            phoneRegex    = re.compile(r'(\d{2,3}\d{3,4}\d{4})', re.VERBOSE)  
            hash_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            
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

            user_data = {
                'id'               : users.id,
                'email'            : users.email,
                'phone'            : users.phone,
                'name'             : users.name,
                'profile_image_url': users.profile_image_url
            }

            if bcrypt.checkpw(password.encode('utf-8'), get_pw) :
                access_token    = jwt.encode({'user_id' : users.id}, SECRET, algorithm = ALGORITHM).decode('utf-8')
                return JsonResponse ({"message":"SUCCESS",'authorization':access_token, 'user_data' : user_data },status=200)

            return JsonResponse({"message":"INVALID EMAIL OR PASSWORD"},status=400)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)

class KakaoLoginView(View):
    def post(self, request):
        try:
            API_HOST = 'https://kapi.kakao.com/v2/user/me'

            access_token    = request.headers.get('Authorization')
            print(access_token)
            request_headers = {'Authorization' : f'Bearer {access_token}'}

            response  = requests.get(API_HOST, headers = request_headers)
            user_data = json.loads(response.text)['kakao_account']

            if not User.objects.filter(email = user_data['email']).exists():
                User.objects.create(
                    email             = user_data['email'],
                    password          = '',
                    phone             = '',
                    name              = user_data['profile']['nickname'],
                    profile_image_url = user_data['profile']['profile_image_url']
                )

            users = User.objects.get(email = user_data['email'])
            user_data = {
                'id'               : users.id,
                'email'            : users.email,
                'phone'            : users.phone,
                'name'             : users.name,
                'profile_image_url': users.profile_image_url
            }
            winted_token    = jwt.encode({'user_id' : users.id}, SECRET, algorithm = ALGORITHM).decode('utf-8')

            return JsonResponse({'message' : 'SUCCESS', 'authorization': winted_token, 'user_data' : user_data}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except ValueError as ex:
            return JsonResponse({'message' : 'VALUE_ERROR_' + ex.args[0]}, status = 400)

            
class LikeView(View):
    @token_check
    def post(self , request):
        try:
            data            = json.loads(request.body)
            company_id      = data["company_id"]
            user_id         = request.user.id   
            get_user_id     = User.objects.get(id=user_id).id
            get_company_id  = Company.objects.get(id=company_id).id
            like_filter     = Like.objects.filter (user_id = get_user_id , company_id=get_company_id)
            
            if get_user_id and get_company_id and not like_filter:
                Like.objects.create(user_id = get_user_id , company_id=get_company_id)
                return JsonResponse({"message":"SUCCESS"},status=201)
            
            return JsonResponse({"message":"id or like_duplication INVALID"},status=400)
        
        except Company.DoesNotExist:
            return JsonResponse({"message":"user_id or company_id INVALID"},status=400)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)

    @token_check
    def delete(self , request):
        try:
            data            = json.loads(request.body)
            company_id      = data["company_id"]
            user_id         = request.user.id

            get_user_id     = User.objects.get(id=user_id).id
            get_company_id  = Company.objects.get(id=company_id).id
            
            if get_user_id and get_company_id :
                Like.objects.get(user_id = get_user_id , company_id=get_company_id).delete()
                return JsonResponse({"message":"SUCCESS"},status=201)
            
            return JsonResponse({"message":"user_id or company_id INVALID"},status=400)
        
        except Like.DoesNotExist:
            return JsonResponse({"message":"user_id or company_id INVALID"},status=400)

        except KeyError :
            return JsonResponse({"message":"Key_Error"},status=400)
             

    @token_check
    def get(self , request):
        user_id = request.user.id 
        
        company_list=[
                { 
                "id"            :applied_status.id , 
                "title"         :applied_status.title ,
                "name"          :applied_status.name,
                "city"          :applied_status.district.city.name,   
                "compensation"  :applied_status.compensation.recommender+applied_status.compensation.applicant,
                "like_count"    :applied_status.likes_count,
                "response_rate" :applied_status.response_rate.rate,
                "image_url"     :applied_status.image_url   
            } for applied_status in  User.objects.get(id=user_id).likes.select_related('district__city', 'compensation', 'response_rate')]

        return JsonResponse( {"message":"SUCCESS","job_list":company_list},status=201)

class TagView(View):
   
    @token_check 
    def post(self , request):
        data           = json.loads(request.body) 
        user_id             = request.user.id   
        get_user_id         = User.objects.get(id=user_id).id
        filter_delete       = User.objects.get(id=user_id)
        usertagfilter_table = User.objects.get(id=user_id).usertagfilter_set.all()

        if  "tag_list" in data : 
            tag_list  = data["tag_list"]

            for filter in UserTagFilter.objects.filter(user_id=user_id):
                if filter.tag.id not in tag_list:
                    filter.delete()

            for tag in tag_list:
                if not UserTagFilter.objects.filter(user_id=user_id, tag_id=tag).exists():
                    UserTagFilter.objects.create(
                        user_id = user_id,
                        tag_id  = tag
                    )

        if  "district_list" in data :
            district_list = data ["district_list"]

            for filter in UserDistrictFilter.objects.filter(user_id=user_id):
                if filter.district.id not in district_list:
                    filter.delete()

            for district in district_list:
                if not UserDistrictFilter.objects.filter(user_id=user_id, district_id=district).exists():
                    
                    UserDistrictFilter.objects.create(user_id= user_id, district_id = district)

        if  "career_list" in data :
            career_list  = data ["career_list"] 

            for filter in UserCareerFilter.objects.filter(user_id=user_id):
                if filter.career.id not in career_list:
                    filter.delete()

            for career in career_list:
                if not UserCareerFilter.objects.filter(user_id=user_id, career_id=career).exists():
                    UserCareerFilter.objects.create(user_id= user_id, career_id = career)

        return JsonResponse({"message":"SUCCESS"},status=201)
        
    @token_check
    def get(self , request):
        user_id = request.user.id 
        
        tag_list=[
                { 
                "id"    :tags.id , 
                "name"  :tags.name 
            } for tags in  User.objects.get(id=user_id).tag_filters.select_related()]
            
        district_list=[
                {     
                "id"       :district.id , 
                "city"     :district.city.name,
                "district" :district.name           
            } for district in  User.objects.get(id=user_id).district_filters.select_related()]
        
        career_list=[
                {     
                "id"   :career.id , 
                "name" :career.name            
            } for career in  User.objects.get(id=user_id).career_filters.select_related()]
        
        return JsonResponse( {"message":"SUCCESS","tag_list":tag_list , "district_list" :district_list ,"career_list" :career_list},status=201)