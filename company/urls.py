from django.urls import path

from company.views import (
    ExploreCategoryView,
    CompanyListView,
    CompanyListDetailView,
    FilterView,
    JobSalaryView
)
urlpatterns = [
    path('/category', ExploreCategoryView.as_view()),
    path('', CompanyListView.as_view()),
    path('/<int:company_id>', CompanyListDetailView.as_view()),
    path('/filter/<str:filter_type>', FilterView.as_view()),
    path('/salary/<int:main_category_id>/<int:sub_category_id>', JobSalaryView.as_view())
]