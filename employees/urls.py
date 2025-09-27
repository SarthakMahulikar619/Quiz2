from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    DepartmentViewSet, PositionViewSet, EmployeeViewSet,
    health_check, dashboard
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('api/', include(router.urls)),
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    path('health/', health_check, name='health_check'),
]
