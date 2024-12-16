from django.contrib import admin
from .models import User, Role, Permission, RolePermission, AuditLog

# Customize the display of the User model in the admin panel
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)
    ordering = ('id',)

# Customize the Role model display
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

# Customize the Permission model display
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'resource', 'action',)
    search_fields = ('resource', 'action',)

# Customize the RolePermission model display
@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'permission',)
    search_fields = ('role__name', 'permission__resource', 'permission__action')

# Customize the AuditLog model display (if implemented)
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'resource', 'action', 'outcome', 'timestamp')
    search_fields = ('user__username', 'resource', 'action')
    list_filter = ('outcome', 'timestamp')
    ordering = ('-timestamp',)
