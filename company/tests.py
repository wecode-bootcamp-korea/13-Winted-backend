from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

from django.test.utils import captured_stderr

from company.models import (
    Company, 
    CompanyTag, 
    Compensation, 
    District,
    ExploreMainCategory, 
    ExploreSubCategory, 
    ResponseRate, 
    Salary,
    TagCategory,
    Tag,
    City,
    Career,
    MapInformation
)

class ExploreCategoryTest(TestCase): # 탐색페이지 카테고리 테스트
    def setUp(self):
        ExploreMainCategory.objects.create(
            id        = 1,
            name      = 'main',
            image_url = 'image'
        )

        ExploreSubCategory.objects.create(
            id          = 1,
            name        = 'sub_cate1',
            image_url   = 'image',
            category_id = 1
        )

        ExploreSubCategory.objects.create(
            id          = 2,
            name        = 'sub_cate2',
            image_url   = 'image',
            category_id = 1
        )
    
    def tearDown(self):
        ExploreMainCategory.objects.all().delete()
        ExploreSubCategory.objects.all().delete()
    
    def test_explorecategory_get_success(self):
        client = Client()
        response = client.get('/company/category')
        self.assertEqual(response.json(),
            {   'message': 'SUCCESS',
                "category_list" :[
                    {
                        "id": 1,
                        "title": "main",
                        "image_url": "image",
                        "sub_category": [
                            {
                                "id": 1,
                                "title": "sub_cate1",
                                "image_url": "image",
                                "category_id" : 1
                            },
                            {
                                "id": 2,
                                "title": "sub_cate2",
                                "image_url": "image",
                                "category_id" : 1
                            }
                        ]
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_explorecategory_get_not_found(self):
        client = Client()
        response = client.get('/company/category/')
        self.assertEqual(response.status_code, 404)

class FilterTest(TestCase): # 필터리스트 테스트
    def setUp(self):
        TagCategory.objects.create(
            id   = 1, 
            name = 'tag_cate1'
        )
        Tag.objects.create(
            id          = 1, 
            name        = 'tag1', 
            category_id = 1
        )

        City.objects.create(
            id   = 1, 
            name = 'city1'
        )
        District.objects.create(
            id      = 1, 
            name    = 'district1', 
            city_id = 1
        )

        Career.objects.create(
            id   = 1, 
            name = 'career1'
        )
    
    def tearDown(self):
        TagCategory.objects.all().delete()
        Tag.objects.all().delete()
        City.objects.all().delete()
        District.objects.all().delete
    
    def test_filter_tag_get_success(self):
        client = Client()
        response = client.get('/company/filter/tag')
        self.assertEqual(response.json(),
            {   
                "message": 'SUCCESS',
                "tag_list": [{
                    'id' : 1,
                    'name' : 'tag_cate1',
                    'tags' : [{
                        'id' : 1,
                        'name' : 'tag1'
                    }]
                }]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_filter_tag_get_not_found(self):
        client = Client()
        response = client.get('/company/filter/tag/')
        self.assertEqual(response.status_code, 404)

    def test_filter_city_get_success(self):
        client = Client()
        response = client.get('/company/filter/city')
        self.assertEqual(response.json(),
            {   
                "message": 'SUCCESS',
                "city_list": [{
                    'id' : 1,
                    'name' : 'city1',
                    'districts' : [{
                        'id' : 1,
                        'name' : 'district1'
                    }]
                }]
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_filter_city_get_not_found(self):
        client = Client()
        response = client.get('/company/filter/city/')
        self.assertEqual(response.status_code, 404)

    def test_filter_career_get_success(self):
        client = Client()
        response = client.get('/company/filter/career')
        self.assertEqual(response.json(),
            {   
                "message": 'SUCCESS',
                "career_list": [{
                    'id' : 1,
                    'name' : 'career1'
                }]
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_filter_career_get_not_found(self):
        client = Client()
        response = client.get('/company/filter/career/')
        self.assertEqual(response.status_code, 404)
    
    def test_filter_invalid_filter_type(self):
        client = Client()
        response = client.get('/company/filter/tag1')
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_FILTER_TYPE'
            }
        )
        self.assertEqual(response.status_code, 400)

class CompanyListTest(TestCase):
    def setUp(self):
        Career.objects.create(
            id   = 1, 
            name = 'career'
        )

        Compensation.objects.create(
            id          = 1, 
            recommender = 100, 
            applicant   = 100
        )

        City.objects.create(
            id   = 1, 
            name = 'city'
        )

        District.objects.create(
            id      = 1, 
            name    = 'district', 
            city_id = 1
        )

        ExploreMainCategory.objects.create(
            id   = 1, 
            name = 'main_cate'
        )

        ExploreSubCategory.objects.create(
            id          = 1, 
            name        = 'sub_cate', 
            category_id = 1
        )

        ResponseRate.objects.create(
            id   = 1, 
            rate = 90
        )

        Company.objects.create(
            id                      = 1,
            name                    = 'name',
            title                   = 'title',
            likes_count             = 100,
            contents                = 'contents',
            image_url               = 'image_url, image_url2',
            deadline                = 'deadline',
            address                 = 'address',
            career_id               = 1,
            compensation_id         = 1,
            district_id             = 1,
            explore_sub_category_id = 1,
            response_rate_id        = 1
        )

        TagCategory.objects.create(
            id   = 1, 
            name = 'tag_cate'
        )

        Tag.objects.create(
            id          = 1, 
            name        = 'tag', 
            category_id = 1
        )

        CompanyTag.objects.create(
            id         = 1, 
            company_id = 1, 
            tag_id     = 1
        )

        MapInformation.objects.create(
            id         = 1,
            latitude   = 100,
            longitude  = 100,
            company_id = 1
        )

    def tearDown(self):
        Career.objects.all().delete()
        Compensation.objects.all().delete()
        City.objects.all().delete()
        District.objects.all().delete()
        ExploreMainCategory.objects.all().delete()
        ExploreSubCategory.objects.all().delete()
        ResponseRate.objects.all().delete()
        Company.objects.all().delete()
        Tag.objects.all().delete()
        CompanyTag.objects.all().delete()
        MapInformation.objects.all().delete()

    def test_companylist_get_success(self):
        client = Client()
        response = client.get('/company')
        self.assertEqual(response.json(),
            {
                "message": "SUCCESS",
                "job_list" : [{
                    'id'            : 1,
                    'title'         : 'title',
                    'name'          : 'name',
                    'response_rate' : 90,
                    'city'          : 'city',
                    'compensation'  : 200,
                    'likes_count'   : 100,
                    'image_url'     : 'image_url',
                    'like_status'   : False
                }]
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_companylist_get_not_found(self):
        client = Client()
        response = client.get('/company/')
        self.assertEqual(response.status_code, 404)
    
    def test_companylistdetail_get_success(self):
        client = Client()
        response = client.get('/company/1')
        self.assertEqual(response.json(),
            {
                "message": "SUCCESS",
                "job_detail" : {
                    'id'                       : 1,
                    'title'                    : 'title',
                    'name'                     : 'name',
                    'response_rate'            : 90,
                    'city'                     : 'city',
                    'compensation_recommender' : 100,
                    'compensation_applicant'   : 100,
                    'likes_count'              : 100,
                    'contents'                 : 'contents',
                    'deadline'                 : 'deadline',
                    'address'                  : 'address',
                    'location'                 : ['100.000000', '100.000000'],
                    'like_status'              : False,
                    'image_url'                : ['image_url', ' image_url2'],
                    'tag_list' : [{
                        'id'   : 1,
                        'name' : 'tag'
                    }]
                }
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_companylistdetail_get_not_found(self):
        client = Client()
        response = client.get('/company/s')
        self.assertEqual(response.status_code, 404)

class JobSalaryTest(TestCase):
    def setUp(self):
        ExploreMainCategory.objects.create(
            id   = 1, 
            name = 'main'
        )

        ExploreSubCategory.objects.create(
            id          = 1, 
            name        = 'sub', 
            category_id = 1
        )

        Career.objects.create(
            id   = 1, 
            name = 'career'
        )

        Salary.objects.create(
            id               = 1, 
            career_id        = 1,
            main_category_id = 1,
            sub_category_id  = 1,
            salary           = 1000
        )
    
    def tearDown(self):
        ExploreMainCategory.objects.all().delete()
        ExploreSubCategory.objects.all().delete()
        Career.objects.all().delete()
        Salary.objects.all().delete()

    def test_jobsalary_get_success(self):
        client = Client()
        response = client.get('/company/salary/1/1')
        self.assertEqual(response.json(),
            {
                "message": "SUCCESS",
                "salary_list": [{
                    'id'               : 1,
                    'salary'           : 1000,
                    'main_category_id' : 1,
                    'sub_category_id'  : 1,
                    'career_id'        : 1
                }]
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_jobsalary_get_not_found(self):
        client = Client()
        response = client.get('/company/salary/1/1/')
        self.assertEqual(response.status_code, 404)
