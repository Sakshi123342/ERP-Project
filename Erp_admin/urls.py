# Bank/urls.py

from django.urls import path
from .views import AdminModelRegistration, AdminModelLoginView
from .views import GeneralDetailsListCreate,GeneralDetailsRetrieveUpdateDestroy

urlpatterns = [
    path('api/auth/register/', AdminModelRegistration.as_view(), name='bank-register'),
    path('api/auth/login/', AdminModelLoginView.as_view(), name='bank-login'),
    path('user/', GeneralDetailsListCreate.as_view(), name='bank-login'),
    path('user/<int:pk>/', GeneralDetailsRetrieveUpdateDestroy.as_view(), name='bank-login'),
]
