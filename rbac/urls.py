from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rbac.views import RoleViewSet, PermissionViewSet, UserViewSet, AuditLogViewSet, AccessValidationView

router = DefaultRouter()
router.register(r'roles', RoleViewSet)

# router.register('roles', RoleViewSet, basename='role')
router.register('permissions', PermissionViewSet, basename='permission')
router.register('users', UserViewSet, basename='user')
router.register('audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('', include(router.urls)),
    path('access/validate/', AccessValidationView.as_view(), name='access-validate'),
]

