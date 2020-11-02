from django.db import models

class Resume(models.Model):
    title        = models.CharField(max_length=50)
    status       = models.BooleanField(default=False)
    create_time  = models.DateField(auto_now_add=True)
    user         = models.ForeignKey('user.User', on_delete=models.CASCADE)
    introduction = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'resumes'

class UserCareer(models.Model):
    company_name    = models.CharField(max_length=50)
    position        = models.CharField(max_length=50)
    year_of_service = models.DateField(max_length=50)
    resume          = models.ForeignKey(Resume, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_careers'

class Education(models.Model):
    university_name = models.CharField(max_length=50)
    major           = models.CharField(max_length=50)
    subject         = models.CharField(max_length=50)
    year_of_service = models.DateField(max_length=50)
    resume          = models.ForeignKey(Resume, on_delete=models.CASCADE)

    class Meta:
        db_table = 'educations'

class Award(models.Model):
    activity_name   = models.CharField(max_length=50)
    detail          = models.CharField(max_length=50)
    year_of_service = models.DateField(max_length=50)
    resume          = models.ForeignKey(Resume, on_delete=models.CASCADE)

    class Meta:
        db_table = 'awards'

class ForeignLanguage(models.Model):
    language = models.CharField(max_length=50)
    level    = models.CharField(max_length=50)
    resume   = models.ForeignKey(Resume, on_delete=models.CASCADE)

    class Meta:
        db_table = 'foreign_languages'