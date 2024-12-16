
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rbac.models import Role,User,Permission,AuditLog
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rbac.models import RolePermission  # Import the RolePermission model
from rest_framework.viewsets import ReadOnlyModelViewSet

from rbac.serializers import RoleSerializer,PermissionSerializer,UserSerializer,AuditLogSerializer
from rbac.models import Role

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def assign_permission(self, request, pk=None):
        """
        Assign a permission to a role
        """
        role = self.get_object()
        permission_id = request.data.get('permission_id')

        # Validate the permission ID
        if not permission_id:
            return Response({
                'success': False,
                'message': 'Permission ID is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get the permission object
        permission = get_object_or_404(Permission, id=permission_id)

        # Check if the RolePermission already exists
        role_permission, created = RolePermission.objects.get_or_create(role=role, permission=permission)

        if created:
            return Response({
                'success': True,
                'message': 'Permission assigned successfully.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Permission already assigned to this role.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser])
    def permissions(self, request, pk=None):
        """
        Retrieve permissions assigned to a specific role
        """
        role = self.get_object()
        role_permissions = RolePermission.objects.filter(role=role)
        permissions = [rp.permission for rp in role_permissions]
        permissions_data = [{"id": p.id,"resource": p.resource, "action": p.action,"description":p.description} for p in permissions]

        return Response({
            "success": True,
            "message": "Permissions retrieved successfully.",
            "data": permissions_data
        })
            
            
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Create user object with hashed password
            user = User(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            user.set_password(serializer.validated_data['password'])  # Hash the password
            user.save()
            return Response({
                'success': True,
                'message': 'User created successfully.',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'User list retrieved successfully.',
            'data': serializer.data
        })

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def assign_role(self, request, pk=None):
        user = self.get_object()
        role_id = request.data.get('role_id')
        role = get_object_or_404(Role, id=role_id)
        user.role = role
        user.save()
        return Response({'success': True, 'message': 'Role assigned successfully.'})


class AuditLogViewSet(ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """
        Allow filtering by user or time range (e.g., past N days).
        """
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)

        return queryset
            
class AccessValidationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        resource = request.data.get('resource')
        action = request.data.get('action')

        if not resource or not action:
            return Response({
                "success": False,
                "message": "Both 'resource' and 'action' fields are required."
            }, status=400)
        print(user.role)
        if not user.role:
            return Response({
                "success": False,
                "message": "User has no assigned role."
            }, status=403)

        # Check if the role has permission for the resource and action
        has_permission = RolePermission.objects.filter(
            role=user.role, 
            permission__resource=resource, 
            permission__action=action
        ).exists()

        if has_permission:
            return Response({
                "success": True,
                "message": "Access granted."
            }, status=200)
        else:
            return Response({
                "success": False,
                "message": "Access denied."
            }, status=403)

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new permission.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            permission = serializer.save()
            return Response({
                "success": True,
                "message": "Permission created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
