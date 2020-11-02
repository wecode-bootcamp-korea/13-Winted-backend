import json

from django.db     import transaction
from django.http   import JsonResponse
from django.views  import View

from user.utils    import token_check
from user.models   import User
from resume.models import (
    Resume, 
    UserCareer, 
    Education, 
    Award, 
    ForeignLanguage,
)

class ResumeListView(View): # 이력서 리스트
    @token_check
    def post(self, request):
        try:
            user         = User.objects.get(id = request.user.id)
            resume_count = Resume.objects.filter(user = user.id).count()

            Resume.objects.create(
                title        = user.name + str(resume_count + 1),
                status       = False,
                introduction = '',
                user_id      = user.id
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
    
    @token_check
    def get(self, request):
        resume_list = [{
            'id'          : resume.id,
            'title'       : resume.title,
            'status'      : resume.status,
            'create_time' : resume.create_time
        } for resume in Resume.objects.filter(user = request.user.id)]

        return JsonResponse({'message' : 'SUCCESS', 'resume_list' : resume_list}, status = 200)
    
    @token_check
    def delete(self, request):
        try:
            data = json.loads(request.body)

            if Resume.objects.filter(id = data['id']).exists():
                Resume.objects.get(id = data['id']).delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)    

class ResumeDetailListView(View): # 이력서 상세정보
    @token_check
    def get(self, request, resume_id):
        resume = Resume.objects.get(id = resume_id)

        resume_detail = {
            'id'           : resume.id,
            'title'        : resume.title,
            'status'       : resume.status,
            'introduction' : resume.introduction,
            'career_list'  : [{
                'id'           : career.id,
                'company_name' : career.company_name,
                'position'     : career.position,
                'start_date'   : career.start_date,
                'end_date'     : career.end_date
            } for career in resume.usercareer_set.all()],

            'education_list' : [{
                'id'         : education.id,
                'university' : education.university_name,
                'major'      : education.major,
                'subject'    : education.subject,
                'start_date' : education.start_date,
                'end_date'   : education.end_date
            } for education in resume.education_set.all()],

            'award_list' : [{
                'id'       : award.id,
                'activity' : award.activity_name,
                'detail'   : award.detail,
                'date'     : award.date
            } for award in resume.award_set.all()],

            'language_list' : [{
                'id'       : language.id,
                'language' : language.language,
                'level'    : language.level
            } for language in resume.foreignlanguage_set.all()]
        }

        return JsonResponse({'message' : 'SUCCESS', 'resume_detail' : resume_detail}, status = 200)
    
    @token_check
    @transaction.atomic
    def patch(self, request, resume_id):
        try:
            data   = json.loads(request.body)
            resume = Resume.objects.get(id = resume_id)

            resume.title        = data['title']
            resume.status       = data['status']
            resume.introduction = data['introduction']
            resume.save()

            if data['career_list']:
                for career in data['career_list']:
                    if resume.usercareer_set.filter(id = career['id']).exists():
                        career.company_name = data['company_name']
                        career.position     = data['position']
                        career.start_date   = data['career_start_date']
                        career.end_date     = data['career_end_date']
                        career.save()

            if data['education_list']:
                for education in data['education_list']:
                    if resume.education_set.filter(id = education['id']).exists():
                        education.university_name = data['university_name']
                        education.major           = data['major']
                        education.subject         = data['subject']
                        education.start_date      = data['education_start_date']
                        education.end_date        = data['education_end_date']
                        education.save()
                    
            if data['award_list']:
                for award in data['award_list']:
                    if resume.education_set.filter(id = award['id']).exists():
                        award.activity_name  = data['activity_name']
                        award.detail         = data['detail']
                        award.date           = data['award_date']
                        award.save()
                    
            if data['language_list']:
                for language in data['language_list']:
                    if resume.foreignlanguage_set.filter(id = language['id']).exists():
                        language.language = data['language']
                        language.level    = data['level']
                        language.save()
            
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

class UserCareerView(View): # 경력 등록,삭제
    def post(self, request, resume_id):
        try:
            data = json.loads(request.body)

            UserCareer.objects.create(
                company_name = data['company_name'],
                position     = data['position'],
                start_date   = data['career_start_date'],
                end_date     = data['career_end_date'],
                resume_id    = resume_id
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
    
    def delete(self, request, resume_id):
        try:
            data = json.loads(request.body)

            if UserCareer.objects.filter(id = data['career_id']).exists():
                UserCareer.objects.get(id = data['career_id']).delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

class EducationView(View): # 학력 등록, 삭제
    def post(self, request, resume_id):
        try:
            data = json.loads(request.body)

            Education.objects.create(
                university_name = data['university_name'],
                major           = data['major'],
                subject         = data['subject'],
                start_date      = data['start_date'],
                end_date        = data['end_date'],
                resume_id       = resume_id
            )
            
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

    def delete(self, request, resume_id):
        try:
            data = json.loads(request.body)

            if Education.objects.filter(id = data['education_id']).exists():
                Education.objects.get(id = data['education_id']).delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

class AwardView(View): # 수상내역 등록, 삭제
    def post(self, request, resume_id):
        try:
            data = json.loads(request.body)

            Award.objects.create(
                activity_name = data['activity_name'],
                detail        = data['detail'],
                date          = data['award_date'],
                resume_id     = resume_id
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
    
    def delete(self, request, resume_id):
        try:
            data = json.loads(request.body)

            if Award.objects.filter(id = data['award_id']).exists():
                Award.objects.get(id = data['award_id']).delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

class ForeignLanguageView(View): # 외국어 등록, 삭제
    def post(self, request, resume_id):
        try:
            data = json.loads(request.body)

            ForeignLanguage.objects.create(
                language   = data['language'],
                level      = data['level'],
                resume_id  = resume_id
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)

    def delete(self, request, resume_id):
        try:
            data = json.loads(request.body)

            if ForeignLanguage.objects.filter(id = data['language_id']).exists():
                ForeignLanguage.objects.get(id = data['language_id']).delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)