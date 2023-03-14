from django.urls import path
from .import  views
from .views import SearchResultsListView

urlpatterns=[
     
     path('jobseeker_register/',views.jobseeker_register.as_view(), name='jobseeker_register'),
     path('company_register/',views.company_register.as_view(), name='company_register'),
     path('login/',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
     path('jobseeker_profile_edit/', views.jobseeker_profile_edit, name='jobseeker_profile_edit'),
     path('company_profile_edit/', views.company_profile_edit, name='company_profile_edit'),
     path('jobseeker_dashboard/<int:user_id>/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
     path('company_dashboard/<int:user_id>/', views.company_dashboard, name='company_dashboard'),
     path('jobseeker_dashboard_for_company/<int:user_id>/', views.jobseeker_dashboard_for_company, name='jobseeker_dashboard_for_company'),
     
    
     path('jobseekers_profiles_view/', views.jobseekers_profiles_view, name='jobseekers_profiles_view'),
     path('search_results/', SearchResultsListView.as_view(), name='search_results'),

]