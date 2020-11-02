from django.db import models

class RecommendCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'recommend_categories'

class Recommender(models.Model):
    contents    = models.CharField(max_length=300)
    category    = models.ForeignKey(RecommendCategory, on_delete=models.CASCADE)
    create_time = models.DateField(auto_now_add=True)
    from_user   = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='recommend_from_user')
    to_user     = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='recommend_to_user')

    class Meta:
        db_table = 'recommenders'