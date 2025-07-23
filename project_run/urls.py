from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_run.views import (
    get_company_details,
    RunViewSet,
)

router = DefaultRouter()
router.register('api/runs', RunViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/company_details/', get_company_details),
]
