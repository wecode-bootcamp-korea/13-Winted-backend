from user.utils import token_check

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from company.models import (
    Company,
    ExploreMainCategory, Salary,
    TagCategory,
    City,
    Career,
)

class ExploreCategoryView(View): # 탐색페이지 카테고리
    def get(self, request):
        category_list = [{
            'id'           : main_cate.id,
            'title'        : main_cate.name,
            'image_url'    : main_cate.image_url,
            'sub_category'    : [{
                'id'          : sub_cate.id,
                'title'       : sub_cate.name,
                'image_url'   : sub_cate.image_url,
                'category_id' : sub_cate.category_id
            } for sub_cate in main_cate.exploresubcategory_set.all()]
        } for main_cate in ExploreMainCategory.objects.prefetch_related('exploresubcategory_set').all()]

        return JsonResponse({'message' : 'SUCCESS', 'category_list' : category_list}, status = 200)

class FilterView(View): # 탐색페이지 필터(태그,지역,경력) 리스트
    def get(self, request, filter_type):
        if filter_type == 'tag':
            tag_list = [{
                'id'   : category.id,
                'name' : category.name,
                'tags'     : [{
                    'id'   : tag.id,
                    'name' : tag.name
                } for tag in category.tag_set.all()]
            } for category in TagCategory.objects.prefetch_related('tag_set').all()]

            return JsonResponse({'message' : 'SUCCESS', 'tag_list' : tag_list}, status = 200)
        
        elif filter_type == 'city':
            city_list = [{
            'id'   : city.id,
            'name' : city.name,
            'districts' :[{
                'id'    : district.id,
                'name'  : district.name
            } for district in city.district_set.all()]
        } for city in City.objects.prefetch_related('district_set').all()]

            return JsonResponse({'message' : 'SUCCESS', 'city_list' : city_list}, status = 200)

        elif filter_type == 'career':
            career_list = [{
            'id'   : career.id,
            'name' : career.name
        } for career in Career.objects.all()]

            return JsonResponse({'message' : 'SUCCESS', 'career_list' : career_list}, status = 200)
        
        else:
            return JsonResponse({'message' : 'INVALID_FILTER_TYPE'}, status = 400)

class CompanyListView(View): # 탐색페이지 회사공고 리스트
    @token_check
    def get(self, request):
        access_token = request.headers.get('Authorization', None)
        user         = request.user if access_token != None else None

        main_category_id = request.GET.get('main')
        sub_category_id  = request.GET.get('sub')
        sorting          = request.GET.get('job_sort')
        city_id          = request.GET.get('city')
        career_id        = request.GET.get('career')
        offset           = int(request.GET.get('offset', 0))
        limit            = int(request.GET.get('limit', 16))
        tags             = request.GET.getlist('tag')
        tags_dict        = {'company_tag__in' : tags}

        q = Q()

        if main_category_id:
            q.add(Q(explore_sub_category__category = main_category_id), q.AND)
        if sub_category_id:
            q.add(Q(explore_sub_category = sub_category_id), q.AND)
        if city_id:
            q.add(Q(district__city = city_id), q.AND)
        if career_id and career_id != 1:
            q.add(Q(career_id__gte = career_id), q.AND)

        if not sorting:
            sorting = 'popularity'

        sort_type = {
            'popularity'   : '-likes_count',
            'compensation' : '-compensation__recommender',
            'response'     : '-response_rate__rate'
        }

        if tags:
            company_list = Company.objects.select_related(
                'response_rate', 'district__city', 'compensation'
                ).order_by(sort_type[sorting]).filter(q, **tags_dict)
        else:
            company_list = Company.objects.select_related(
                'response_rate', 'district__city', 'compensation'
                ).order_by(sort_type[sorting]).filter(q)

        like_list = []
        if user != None:
            like_list = [like.id for like in user.likes.all()]

        job_list = [{
            'id'            : job.id,
            'title'         : job.title,
            'name'          : job.name,
            'response_rate' : job.response_rate.rate,
            'city'          : job.district.city.name,
            'compensation'  : job.compensation.applicant + job.compensation.recommender,
            'likes_count'   : job.likes_count,
            'image_url'     : job.image_url.split(',')[0],
            'likes_status'  : True if (user != None) and (job.id in like_list) else False
        } for job in company_list[offset:limit]]
        return JsonResponse({'message' : 'SUCCESS', 'job_list' : job_list}, status = 200)

class CompanyListDetailView(View): # 회사공고 상세페이지
    @token_check
    def get(self, request, company_id):
        access_token = request.headers.get('Authorization', None)
        user         = request.user if access_token != None else None

        job = Company.objects.select_related('response_rate', 'district__city', 'compensation').get(id = company_id)
        location     = job.mapinformation_set.first()
        company_tags = job.company_tag.all()

        job_detail = {
            'id'                       : job.id,
            'title'                    : job.title,
            'name'                     : job.name,
            'response_rate'            : job.response_rate.rate,
            'city'                     : job.district.city.name,
            'compensation_recommender' : job.compensation.recommender,
            'compensation_applicant'   : job.compensation.applicant,
            'likes_count'              : job.likes_count,
            'contents'                 : job.contents,
            'deadline'                 : job.deadline,
            'address'                  : job.address,
            'location'                 : [location.latitude, location.longitude],
            'likes_status'             : True if (user != None) and (job.likes.exists()) else False,
            'image_url'                : [image for image in job.image_url.split(',')],
            'tag_list' : [{
                'id'   : tag.id,
                'name' : tag.name
            } for tag in company_tags]
        }

        return JsonResponse({'message' : 'SUCCESS', 'job_detail' : job_detail}, status = 200)

class JobSalaryView(View): # 직군별 연봉 조회
    def get(self, request, main_category_id, sub_category_id):
        salary_list = [{
            'id'               : salary.id,
            'salary'           : salary.salary,
            'main_category_id' : salary.main_category.id,
            'sub_category_id'  : salary.sub_category.id,
            'career_id'        : salary.career.id
        } for salary in Salary.objects.select_related(
            'career', 'main_category', 'sub_category').filter(sub_category = sub_category_id, main_category = main_category_id)]

        return JsonResponse({'message' : 'SUCCESS', 'salary_list' : salary_list}, status = 200)
