from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
        

class Permission(models.Model):
    action = models.CharField(max_length=50)  # Example: 'create', 'read', 'update', 'delete'
    resource = models.CharField(max_length=50)  # Example: 'users', 'appointments'
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.action.capitalize()} on {self.resource.capitalize()}"


class RolePermission(models.Model):
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission}"


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')



class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    outcome = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
