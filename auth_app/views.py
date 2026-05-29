from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema

from core.permissions import IsAdmin
from .serializers import UserRegistrationSerializer, UserSerializer


@extend_schema(tags=['Auth'])
class RegisterView(APIView):
    permission_classes = [IsAdmin]

    @extend_schema(request=UserRegistrationSerializer, responses={201: UserSerializer})
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Auth'])
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        return Response(UserSerializer(request.user).data)


@extend_schema(tags=['Auth'])
class LoginView(TokenObtainPairView):
    pass


@extend_schema(tags=['Auth'])
class RefreshView(TokenRefreshView):
    pass
