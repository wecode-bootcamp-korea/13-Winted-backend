from django.db import models

class User(models.Model):
    email    = models.EmailField(max_length=250)
    password = models.CharField(max_length=200)
    phone    = models.CharField(max_length=50,null=True)
    name     = models.CharField(max_length=50,null=True)
    recommender = models.ManyToManyField('self', symmetrical=False, through='recommend.Recommender', related_name='recommenders')

    class Meta:
        db_tables = 'users'

class AppliedStatus(models.Model):
    user    = models.ForeignKey('User',on_delete=models.CASCADE)
    company = models.ForeignKey('company.Company',on_delete=models.CASCADE)

    class Meta:
        db_tables='applied_status'

class Like(models.Model):
    user    = models.ForeignKey('User',on_delete=models.CASCADE)
    company = models.ForeignKey('company.Company',on_delete=models.CASCADE)

    class Meta:
        db_tables='likes'

class UserExploreFilter(models.Model):
    user    = models.ForeignKey('User',on_delete=models.CASCADE)
    tag     = models.ForeignKey('company.Tag',on_delete=models.CASCADE)
    area    = models.ForeignKey('company.Area',on_delete=models.CASCADE)
    career  = models.ForeignKey('company.Careear',on_delete=models.CASCADE)

    class Meta:
        db_tables='User_explore_filters'