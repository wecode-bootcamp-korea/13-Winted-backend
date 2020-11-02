from django.db import models

class ExploreMainCategory(models.Model):
    name      = models.CharField(max_length=50)
    image_url = models.CharField(max_length=200)

    class Meta:
        db_table = 'explore_main_categories'

class ExploreSubCategory(models.Model):
    name      = models.CharField(max_length=50)
    image_url = models.CharField(max_length=200)
    category  = models.ForeignKey(ExploreMainCategory, on_delete = models.CASCADE)

    class Meta:
        db_table = 'explore_sub_categories'

class TagCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tag_categories'

class Tag(models.Model):
    name     = models.CharField(max_length=50)
    category = models.ForeignKey(TagCategory, on_delete = models.CASCADE)

    class Meta:
        db_table = 'tags'

class City(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'cities'

class District(models.Model):
    name     = models.CharField(max_length=50)
    city     = models.ForeignKey(City, on_delete = models.CASCADE)

    class Meta:
        db_table = 'districts'

class Career(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'careers'

class Compensation(models.Model):
    recommender = models.FloatField()
    applicant   = models.FloatField()

    class Meta:
        db_table = 'compensations'

class ResponseRate(models.Model):
    rate = models.IntegerField(default=0)

    class Meta:
        db_table = 'response_rates'

class Salary(models.Model):
    salary        = models.IntegerField(default=0)
    main_category = models.ForeignKey(ExploreMainCategory, on_delete=models.CASCADE)
    sub_category  = models.ForeignKey(ExploreSubCategory, on_delete=models.CASCADE)
    career        = models.ForeignKey(Career, on_delete=models.CASCADE)

    class Meta:
        db_table = 'salaries'

class Company(models.Model):
    name                 = models.CharField(max_length=50)
    title                = models.CharField(max_length=50)
    likes_count          = models.IntegerField(default=0)
    contents             = models.CharField(max_length=1000)
    image_url            = models.CharField(max_length=200)
    deadline             = models.CharField(max_length=50)
    address              = models.CharField(max_length=50)
    district             = models.ForeignKey(District, on_delete=models.CASCADE)
    compensation         = models.ForeignKey(Compensation, on_delete=models.CASCADE)
    response_rate        = models.ForeignKey(ResponseRate, on_delete=models.CASCADE)
    explore_sub_category = models.ForeignKey(ExploreSubCategory, on_delete=models.CASCADE)
    career               = models.ForeignKey(Career, on_delete=models.CASCADE)
    company_tag          = models.ManyToManyField(Tag, through='CompanyTag', related_name='company_tags')

    class Meta:
        db_table = 'companies'

class CompanyTag(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    tag     = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'company_tags'