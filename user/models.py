from django.db import models

class User(models.Model):
    email             = models.EmailField(max_length=250)
    password          = models.CharField(max_length=200)
    phone             = models.CharField(max_length=50,null=True)
    name              = models.CharField(max_length=50,null=True)
    profile_image_url = models.URLField(max_length=2000)
    recommender       = models.ManyToManyField('self', symmetrical=False, through='recommend.Recommender', related_name='recommenders')
    apllied_status    = models.ManyToManyField('company.Company', through='AppliedStatus', related_name='applied_status')
    likes             = models.ManyToManyField('company.Company', through='Like', related_name='likes')
    tag_filters       = models.ManyToManyField('company.Tag', through='UserTagFilter', related_name='user_tag_filters')
    career_filters    = models.ManyToManyField('company.Career', through='UserCareerFilter', related_name='user_career_filters')
    district_filters  = models.ManyToManyField('company.District', through='UserDistrictFilter', related_name='user_district_filters')

    class Meta:
        db_table = 'users'

class AppliedStatus(models.Model):
    user    = models.ForeignKey('User',on_delete=models.CASCADE)
    company = models.ForeignKey('company.Company',on_delete=models.CASCADE)

    class Meta:
        db_table = 'applied_status'

class Like(models.Model):
    user    = models.ForeignKey('User',on_delete=models.CASCADE)
    company = models.ForeignKey('company.Company',on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'

class UserCareerFilter(models.Model):
    user     = models.ForeignKey('User',on_delete=models.CASCADE)
    career   = models.ForeignKey('company.Career',on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_career_filters'

class UserTagFilter(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    tag  = models.ForeignKey('company.Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_tag_filters'

class UserDistrictFilter(models.Model):
    user      = models.ForeignKey('User', on_delete=models.CASCADE)
    district  = models.ForeignKey('company.District', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_district_filters'