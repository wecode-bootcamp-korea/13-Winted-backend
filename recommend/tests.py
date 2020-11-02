import json
import jwt

from datetime         import datetime
from django.test      import TestCase, Client

from my_settings      import ALGORITHM, SECRET
from recommend.models import RecommendCategory, Recommender
from user.models      import User

token  = jwt.encode({'user_id' : 1}, SECRET, algorithm = ALGORITHM).decode('utf-8')
header = {'HTTP_AUTHORIZATION' : token}

class RecommenderTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(
                id                = 1,
                email             = 'email',
                password          = 'password',
                phone             = 'phone',
                name              = 'user1',
                profile_image_url = 'image'
            ),
             User(
                id                = 2,
                email             = 'email2',
                password          = 'password2',
                phone             = 'phone2',
                name              = 'user2',
                profile_image_url = 'image2'
            ),
            User(
                id                = 3,
                email             = 'email3',
                password          = 'password3',
                phone             = 'phone3',
                name              = 'user3',
                profile_image_url = 'image3'
            )
        ])

        RecommendCategory.objects.bulk_create([
            RecommendCategory(
                id   = 1,
                name = 'category'
            ),
            RecommendCategory(
                id   = 3,
                name = 'category3'
            )
        ])

        Recommender.objects.bulk_create([
            Recommender(
                id           = 1,
                category_id  = 1,
                from_user_id = 1,
                to_user_id   = 2,
                contents     = 'contents'
            ),
             Recommender(
                id           = 2,
                category_id  = 1,
                from_user_id = 2,
                to_user_id   = 1,
                contents     = 'contents'
            )
        ])
    
    def tearDown(self):
        User.objects.all().delete()
        RecommendCategory.objects.all().delete()
        Recommender.objects.all().delete()
    
    def test_recommender_get_success(self):
        client = Client()
        response = client.get('/recommend?type=written', **header)
        self.assertEqual(response.json(),
            {
                "message": "SUCCESS",
                "written_list": [
                    {
                        "id"                : 1,
                        "profile_image_url" : "image2",
                        "user_name"         : "user2",
                        "contents"          : 'contents',
                        "create_time"       : datetime.today().strftime('%Y-%m-%d'),
                        "category"          : "category"
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_recommender_get_not_found(self):
        client = Client()
        response = client.get('/recommend/', **header)
        self.assertEqual(response.status_code, 404)

    def test_recommender_post_success(self):
        client = Client()
        recommend = { 'email' : 'email3', 'name' : 'user3'}
        response = client.post('/recommend', json.dumps(recommend), content_type='application/json', **header)
        self.assertEqual(response.json(),
            {
                'message' : 'SUCCESS'
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_recommender_post_not_existed_user(self):
        client = Client()
        recommend = { 'email' : 'email4', 'name' : 'user4'}
        response = client.post('/recommend', json.dumps(recommend), content_type='application/json', **header)
        self.assertEqual(response.json(),
            {
                'message' : 'NOT_EXISTED_USER'
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_recommender_post_invalid_keys(self):
        client = Client()
        recommend = { 'email3' : 'email', 'name' : 'user3'}
        response = client.post('/recommend', json.dumps(recommend), content_type='application/json', **header)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_email'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_recommender_post_not_found(self):
        client = Client()
        recommend = { 'email' : 'email3', 'name' : 'user3'}
        response = client.post('/recommend/', json.dumps(recommend), content_type='application/json', **header)
        self.assertEqual(response.status_code, 404)
    
    def test_recommender_patch_success(self):
        client = Client()
        recommend = { 'id' : 1 , 'contents' : 'contents' }
        response = client.patch('/recommend', json.dumps(recommend), content_type='application/json', **header)
        self.assertEqual(response.json(),
            {
                'message' : 'SUCCESS'
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_recommender_patch_invalid_keys(self):
        client = Client()
        recommend = { 'idf' : 1 , 'contents' : 'contents' }
        response = client.patch('/recommend', json.dumps(recommend), content_type='application/json', **header)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR_id'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_recommender_patch_not_found(self):
        client = Client()
        recommend = { 'id' : 1 , 'contents' : 'contents' }
        response = client.patch('/recommend/', json.dumps(recommend), content_type='application/json', **header)
        self.assertEqual(response.status_code, 404)
    
    def test_recommender_delete_success(self):
        client = Client()
        response = client.delete('/recommend?id=1', **header)
        self.assertEqual(response.json(),
            {
                'message' : 'SUCCESS'
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_recommender_delete_not_found(self):
        client = Client()
        response = client.delete('/recommend/', **header)
        self.assertEqual(response.status_code, 404)