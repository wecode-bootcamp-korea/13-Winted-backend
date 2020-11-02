import json
import jwt

from django.test   import TestCase, Client
from unittest.mock import patch,MagicMock
from datetime      import datetime

from my_settings   import SECRET, ALGORITHM
from user.models   import User
from resume.models import(
    Resume, 
    UserCareer, 
    Education, 
    Award, 
    ForeignLanguage
)
token  = jwt.encode({'user_id' : 1}, SECRET, algorithm = ALGORITHM).decode('utf-8')
header = {'HTTP_AUTHORIZATION' : token}

class ResumeListTest(TestCase):
    def setUp(self):
        User.objects.create(
            id                = 1,
            email             = 'email',
            password          = 'password',
            phone             = 'phone',
            name              = 'name',
            profile_image_url = 'image'
        )

        Resume.objects.create(
            id           = 1, 
            title        = 'title',
            status       = False,
            introduction = 'introduction',
            user_id      = 1
        )

    def tearDown(self):
        User.objects.all().delete()
        Resume.objects.all().delete()

    def test_resumelist_get_success(self):
        client = Client()
        response = client.get('/resume', content_type = 'application/json', **header)
        self.assertEqual(response.json(),
            {
                'message' : 'SUCCESS',
                'resume_list' : [{
                    'id' : 1,
                    'title' : 'title',
                    'status' : False,
                    'create_time' : datetime.today().strftime('%Y-%m-%d')
                }]
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_resumelist_get_not_found(self):
        client = Client()
        response = client.get('/resume/', **header)
        self.assertEqual(response.status_code, 404)

    def test_resumelist_post_success(self):
        client = Client()
        resume = {
            'title'        : 'title',
            'status'       : False,
            'introduction' : '',
            'user_id'      : 1
        }
        response = client.post('/resume', json.dumps(resume), content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
    
    def test_resumelist_post_not_found(self):
        client = Client()
        resume = {
            'title'       : 'title',
            'status'       : False,
            'introduction' : '',
            'user_id'      : 1
        }
        response = client.post('/resume/', json.dumps(resume), content_type='application/json', **header)
        self.assertEqual(response.status_code, 404)

    def test_resumelist_delete_success(self):
        client = Client()
        resume = { 'id' : 1 }
        response = client.delete('/resume', json.dumps(resume), content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
    
    def test_resumelist_delete_invalid_keys(self):
        client = Client()
        resume = { 'idf' : 1 }
        response = client.delete('/resume', json.dumps(resume), content_type='application/json', **header)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_id'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_resumelist_delete_not_found(self):
        client = Client()
        resume = { 'id' : 1 }
        response = client.delete('/resume/', json.dumps(resume), content_type='application/json', **header)
        self.assertEqual(response.status_code, 404)

class ResumeDetailListTest(TestCase):
    def setUp(self):
        User.objects.create(
            id                = 1,
            email             = 'email',
            password          = 'password',
            phone             = 'phone',
            name              = 'name',
            profile_image_url = 'image'
        )

        Resume.objects.create(
            id           = 1, 
            title        = 'title',
            status       = False,
            introduction = 'introduction',
            user_id      = 1
        )

    def tearDown(self):
        User.objects.all().delete()
        Resume.objects.all().delete()
    
    def test_resumedetail_get_success(self):
        client = Client()
        response = client.get('/resume/1', **header)
        self.assertEqual(response.json(),
            {
                "message": "SUCCESS",
                "resume_detail": {
                    "id"            : 1,
                    "title"         : "title",
                    "status"        : False,
                    "introduction"  : "introduction",
                    "career_list"   : [],
                    "education_list": [],
                    "award_list"    : [],
                    "language_list" : []
                }
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_resumedetail_get_not_found(self):
        client = Client()
        response = client.get('/resume/1/', **header)
        self.assertEqual(response.status_code, 404)

    def test_resumedetail_patch_success(self):
        client = Client()
        resume = {
            'title'          : 'title2',
            'status'         : True,
            'introduction'   : 'introduction2',
            'career_list'    : [],
            'education_list' : [],
            'award_list'     : [],
            'language_list'  : []
        }
        response = client.patch('/resume/1', json.dumps(resume), content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
    
    def test_resumedetail_patch_invalid_keys(self):
        client = Client()
        resume = {
            'title1'         : 'title2',
            'status'         : True,
            'introduction'   : 'introduction2',
            'career_list'    : [],
            'education_list' : [],
            'award_list'     : [],
            'language_list'  : []
        }
        response = client.patch('/resume/1', json.dumps(resume), content_type='application/json', **header)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_title'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_resumedetail_patch_not_found(self):
        client = Client()
        resume = {
            'title'          : 'title2',
            'status'         : True,
            'introduction'   : 'introduction2',
            'career_list'    : [],
            'education_list' : [],
            'award_list'     : [],
            'language_list'  : []
        }
        response = client.patch('/resume/1/', json.dumps(resume), content_type='application/json', **header)
        self.assertEqual(response.status_code, 404)

class QualificationTest(TestCase):
    def setUp(self):
        User.objects.create(
            id                = 1,
            email             = 'email',
            password          = 'password',
            phone             = 'phone',
            name              = 'name',
            profile_image_url = 'image'
        )

        Resume.objects.create(
            id           = 1, 
            title        = 'title',
            status       = False,
            introduction = 'introduction',
            user_id      = 1
        )

        UserCareer.objects.create(
            id           = 1,
            company_name = 'company_name',
            position     = 'position',
            start_date   = '2020-11-08',
            end_date     = '2020-11-08',
            resume_id    = 1
        )

        Education.objects.create(
            id              = 1,
            university_name = 'university_name',
            major           = 'major',
            subject         = 'subject',
            start_date      = '2020-11-08',
            end_date        = '2020-11-08',
            resume_id       = 1
        )

        Award.objects.create(
            id            = 1,
            activity_name = 'activity_name',
            detail        = 'detail',
            date          = '2020-11-08',
            resume_id     = 1
        )

        ForeignLanguage.objects.create(
            id        = 1,
            language  = 'language',
            level     = 'level',
            resume_id = 1
        )

    def tearDown(self):
        Resume.objects.all().delete()
        UserCareer.objects.all().delete()
    
    def test_usercareer_post_success(self):
        client = Client()
        career = {
            'company_name'      : 'company_name',
            'position'          : 'position',
            'career_start_date' : '2020-11-08',
            'career_end_date'   : '2020-11-08',
            'resume_id'         : 1
        }
        response = client.post('/resume/1/career', json.dumps(career), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_usercareer_post_invalid_keys(self):
        client = Client()
        career = {
            'company_namee'     : 'company_name',
            'position'          : 'position',
            'career_start_date' : '2020-11-08',
            'career_end_date'   : '2020-11-08',
            'resume_id'         : 1
        }
        response = client.post('/resume/1/career', json.dumps(career), content_type='application/json')
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_company_name'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_usercareer_post_not_found(self):
        client = Client()
        career = {
            'company_name'     : 'company_name',
            'position'          : 'position',
            'career_start_date' : '2020-11-08',
            'career_end_date'   : '2020-11-08',
            'resume_id'         : 1
        }
        response = client.post('/resume/1/career/', json.dumps(career), content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_usercareer_delete_success(self):
        client = Client()
        career = { 'career_id' : 1 }
        response = client.delete('/resume/1/career', json.dumps(career), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_usercareer_delete_invalid_keys(self):
        client = Client()
        career = { 'career_idf' : 1 }
        response = client.delete('/resume/1/career', json.dumps(career), content_type='application/json')
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_career_id'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_usercareer_delete_not_found(self):
        client = Client()
        career = { 'career_id' : 1 }
        response = client.delete('/resume/1/career/', json.dumps(career), content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_education_post_success(self):
        client = Client()
        education = {
            'university_name' : 'university_name',
            'major'           : 'major',
            'subject'         : 'subject',
            'start_date'      : '2020-11-08',
            'end_date'        : '2020-11-08',
            'resume_id'       : 1
        }
        response = client.post('/resume/1/education', json.dumps(education), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_education_post_invalids_keys(self):
        client = Client()
        education = {
            'university_namde' : 'university_name',
            'major'            : 'major',
            'subject'          : 'subject',
            'start_date'       : '2020-11-08',
            'end_date'         : '2020-11-08',
            'resume_id'        : 1
        }
        response = client.post('/resume/1/education', json.dumps(education), content_type='application/json')
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_university_name'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_education_post_not_found(self):
        client = Client()
        education = {
            'university_name' : 'university_name',
            'major'           : 'major',
            'subject'         : 'subject',
            'start_date'      : '2020-11-08',
            'end_date'        : '2020-11-08',
            'resume_id'       : 1
        }
        response = client.post('/resume/1/education/', json.dumps(education), content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_education_delete_success(self):
        client = Client()
        education = { 'education_id' : 1 }
        response = client.delete('/resume/1/education', json.dumps(education), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_education_delete_invalid_keys(self):
        client = Client()
        education = { 'education_idf' : 1 }
        response = client.delete('/resume/1/education', json.dumps(education), content_type='application/json')
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_education_id'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_education_delete_not_found(self):
        client = Client()
        education = { 'education_id' : 1 }
        response = client.delete('/resume/1/education/', json.dumps(education), content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_award_post_success(self):
        client = Client()
        award = {
            'activity_name' : 'activity_name',
            'detail'        : 'detail',
            'award_date'    : '2020-11-08',
            'resume_id'     : 1
        }
        response = client.post('/resume/1/award', json.dumps(award), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_award_post_invalid_keys(self):
        client = Client()
        award = {
            'activity_name1' : 'activity_name',
            'detail'         : 'detail',
            'award_date'     : '2020-11-08',
            'resume_id'      : 1
        }
        response = client.post('/resume/1/award', json.dumps(award), content_type='application/json')
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_activity_name'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_award_post_not_found(self):
        client = Client()
        award = {
            'activity_name' : 'activity_name',
            'detail'        : 'detail',
            'award_date'    : '2020-11-08',
            'resume_id'     : 1
        }
        response = client.post('/resume/1/award/', json.dumps(award), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_award_delete_success(self):
        client = Client()
        award = { 'award_id' : 1 }
        response = client.delete('/resume/1/award', json.dumps(award), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_award_delete_invalid_keys(self):
        client = Client()
        award = { 'award_idf' : 1 }
        response = client.delete('/resume/1/award', json.dumps(award), content_type='application/json')
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_award_id'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_award_delete_not_found(self):
        client = Client()
        award = { 'award_id' : 1 }
        response = client.delete('/resume/1/award/', json.dumps(award), content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_foreignlanguage_post_success(self):
        client = Client()
        language = {
            'language'  : 'language',
            'level'     : 'level',
            'resume_id' : 1   
        }
        response = client.post('/resume/1/language', json.dumps(language), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_foreignlanguage_post_invalid_keys(self):
        client = Client()
        language = {
            'languagee'  : 'language',
            'level'      : 'level',
            'resume_id'  : 1   
        }
        response = client.post('/resume/1/language', json.dumps(language), content_type='application/json')
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_language'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_foreignlanguage_post_not_found(self):
        client = Client()
        language = {
            'language'  : 'language',
            'level'     : 'level',
            'resume_id' : 1   
        }
        response = client.post('/resume/1/language/', json.dumps(language), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_foreignlanguage_delete_success(self):
        client = Client()
        language = { 'language_id' : 1 }
        response = client.delete('/resume/1/language', json.dumps(language), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_foreignlanguage_delete_invalid_keys(self):
        client = Client()
        language = { 'language_idf' : 1 }
        response = client.delete('/resume/1/language', json.dumps(language), content_type='application/json')
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_language_id'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_foreignlanguage_delete_not_found(self):
        client = Client()
        language = { 'language_id' : 1 }
        response = client.delete('/resume/1/language/', json.dumps(language), content_type='application/json')
        self.assertEqual(response.status_code, 404)