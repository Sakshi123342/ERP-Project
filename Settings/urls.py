# urls.py
from django.urls import path
from . import views
from .views import *
# from .views import UserDetailView



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyModelViewSet

# Initialize the router and register the viewset
router = DefaultRouter()
router.register(r'users', MyModelViewSet, basename='user')


urlpatterns = [
    path('User_RUD/', include(router.urls)),
    path('api/login/', views.login_user, name='login_user'),
    path('api/assign-permission/', views.assign_permissions, name='assign-permissions'),
    path('api/register/', views.register_user, name='register-user'),
    path('api/users-dropdown/', views.get_users_for_dropdown, name='users-dropdown'), 
    path('financial_years/', views.financial_years, name='get_create_financial_years'),  # For GET and POST
    path('financial_years/<int:pk>/', views.financial_years, name='get_update_delete_financial_years'),  # For GET, PUT, DELETE by pk  
    path('schedule-month/', ScheduleMonthAPIView.as_view() , name='schedule-month'),
    path('schedule-month/<int:pk>/', ScheduleMonthAPIView.as_view(), name='schedule-month-updated-delete'),
]