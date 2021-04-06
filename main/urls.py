from django.urls import path
from .views import *


urlpatterns = [


    path('', TestListView.as_view(), name='test_list'),
    path('<int:pk>/', create_statistics, name='create_statistics'),
    path('<int:pk>/statistics/', get_statistics, name='get_statistics'),


    path('completed_tests/', TestCompleteListView.as_view(), name='completed_test_list'),


]