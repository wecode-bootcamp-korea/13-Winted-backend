import json
import requests

from django.http  import JsonResponse
from django.views import View

from user.utils       import token_check
from recommend.models import Recommender
from user.models      import User

class RecommenderView(View):
    @token_check
    def post(self, request): # 지인 추천 하기
        try:
            user_id = request.user.id
            data    = json.loads(request.body)

            if User.objects.filter(email = data['email'], name = data['name']).exists():
                recommender = User.objects.get(email = data['email'], name = data['name'])

                if Recommender.objects.filter(from_user_id = user_id, to_user_id = recommender.id).exists():
                    return JsonResponse({'message' : 'ALREADY_RECOMMENDED_USER'}, status = 200)

                Recommender.objects.create(
                    category_id  = 3,
                    from_user_id = user_id,
                    to_user_id   = recommender.id,
                    contents     = ''
                )

                return JsonResponse({'message' : 'SUCCESS'}, status = 200)
            
            return JsonResponse({'message' : 'NOT_EXISTED_USER'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        
    @token_check
    def get(self, request): # 추천 페이지(내가한추천, 내가받은추천)
        user_id = request.user.id
        recommend_type = request.GET.get('type')

        if recommend_type == 'written': # 내가 한 추천
            written_list = [{
                'id'                : recommender.id,
                'profile_image_url' : recommender.to_user.profile_image_url,
                'user_name'         : recommender.to_user.name,
                'create_time'       : recommender.create_time,
                'category'          : recommender.category.name,
                'contents'          : recommender.contents
            } for recommender in Recommender.objects.select_related('to_user', 'category').filter(from_user = user_id)]

            return JsonResponse({'message' : 'SUCCESS', 'written_list' : written_list}, status = 200)   

        elif recommend_type == 'given': # 내가 받은 추천
            given_list = [{
                'id'                : recommender.id,
                'profile_image_url' : recommender.from_user.profile_image_url,
                'user_name'         : recommender.from_user.name,
                'create_time'       : recommender.create_time,
                'category'          : recommender.category.name,
                'contents'          : recommender.contents
            } for recommender in Recommender.objects.select_related('from_user', 'category').filter(to_user = user_id)]

            return JsonResponse({'message' : 'SUCCESS', 'given_list' : given_list}, status = 200)
        
        else:
            return JsonResponse({'message' : 'INVALID_RECOMMEND_TYPE'}, status = 400)
    
    @token_check
    def patch(self, request): # 추천사 수정 (내가한추천)
        try:
            data = json.loads(request.body)

            recommendation = Recommender.objects.get(id = data['id'])
            recommendation.contents = data['contents']
            recommendation.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
    
    @token_check
    def delete(self, request): # 추천 삭제 (내가한추천)
        recommend_id = request.GET.get('id')

        if Recommender.objects.filter(id = recommend_id).exists():
            Recommender.objects.get(id = recommend_id).delete()

        return JsonResponse({'message' : 'SUCCESS'}, status = 200)

class KakaoMessageView(View):
    def post(self, request):
        
        API_HOST = 'https://kapi.kakao.com/v2/api/talk/memo/send?template_id=40542'

        access_token    = request.headers.get('Authorization')
        request_headers = {'Authorization' : f'Bearer {access_token}'}

        requests.post(API_HOST, headers = request_headers)
        
        return JsonResponse({'message' : 'SUCCESS'}, status = 200)