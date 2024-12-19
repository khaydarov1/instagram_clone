from datetime import datetime
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView, TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from shared.utility import send_email
from .serializers import LoginRefreshSerializer, LogoutSerializer, SignUpSerializer, ChangeUserInformaion, ChangeUserPhotoSerializer, LoginSerializer, TokenRefreshSerializer
from .models import User, DONE, CODE_VERIFIED, NEW, VIA_EMAIL, VIA_PHONE
from django.core.exceptions import ObjectDoesNotExist

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer


class VerifyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = request.data.get('code')

        self.check_verify(user, code)
        return Response(
            data={
                'success': True,
                'auth_status': user.auth_status,
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token']
            }
        )

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        print(verifies)
        if not verifies.exists():
            data = {
                'message': 'Verification code is invalid',
            }
            raise ValidationError(data)

        verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class GetNewVerification(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verificotion(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone_number, code)
        else:
            data = {
                'message': 'Invalid auth type',
            }
            raise ValidationError(data)
        return Response({
            'success': True,
            'message': "Tasdiqlash kodingiz qaytadan jo'natildi",
        })

    @staticmethod
    def check_verificotion(user):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                'message': 'Kodingiz hali ishtalish uchun yaroqli. Biroz kuting!',
            }
            raise ValidationError(data)


class ChangeUserInformationView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeUserInformaion
    http_method_names = ['put', 'patch', 'delete']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(ChangeUserInformationView, self).update(request, *args, **kwargs)
        data = {
            'success': True,
            'messege': "User information updated",
            'auth_status': self.request.user.auth_status,
        }
        return Response(data, status=200)


class ChangeUserPhotoView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeUserPhotoSerializer

    def put(self, request, *args, **kwargs):
        serializer = ChangeUserPhotoSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({
                'success': True,
                'message': "User information updated",
            }, status=200)
        return Response(serializer.errors, status=400)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class LoginRefreshView(TokenRefreshView):
    serializer_class=LoginRefreshSerializer
    
class LogOutView(APIView):
    serializer_class=LogoutSerializer
    permission_classes=[IsAuthenticated,]
    
    def post(self,request,*args, **kwargs):
        serializer=self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token=self.request.data['refresh']
            token=RefreshToken(refresh_token)
            token.blacklist()
            data={
                'success': True,
                'message': 'Loggout'                
            }
            return Response(data, status=205)
        except TokenError:
            return Response(status=400)