from django.urls import path

from django.urls import path
from .views import *

urlpatterns = [
    path('tool-management/',ToolManagementAPIView.as_view(),name='tool-management'),
]