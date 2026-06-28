from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.infrastructure.models import User
from apps.accounts.interfaces.serializers import CurrentUserSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('organization').all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['username','email','first_name','last_name']
    filterset_fields = ['organization','role','is_active','is_staff']

class MeAPIView(APIView):
    def get(self, request):
        return Response({'success': True, 'data': CurrentUserSerializer(request.user).data})
