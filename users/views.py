from datetime import datetime
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from shared.utility import send_email, check_email_or_phone
from .serializers import LoginRefreshSerializer, LogoutSerializer, \
    SignUpSerializer, ChangeUserInformaion, ChangeUserPhotoSerializer, \
    LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .models import User, CODE_VERIFIED, NEW, VIA_EMAIL, VIA_PHONE
from django.core.exceptions import ObjectDoesNotExist


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer


class VerifyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
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
    def get(self):
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

    @staticmethod
    def put(request):
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
    serializer_class = LoginRefreshSerializer


class LogOutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'success': True,
                'message': 'Loggout'
            }
            return Response(data, status=205)
        except TokenError:
            return Response(status=400)


class ForgotPasswodView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = ForgotPasswordSerializer

    def post(self):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email_or_phone = serializer.validated_data.get('email_or_phone')
        user = send_email.validated_data.get('user')

        if check_email_or_phone(email_or_phone) == 'phone':
            code = user.create_verify_code(VIA_PHONE)
            send_email(email_or_phone, code)

        elif check_email_or_phone(email_or_phone) == 'email':
            code = user.create_verify_code(VIA_EMAIL)
            send_email(email_or_phone, code)

        return Response({
            "success": True,
            'message': "Tasdiqlash kodi mavaffiqiyatli yuborldi",
            "access": user.token()['access'],
            'refresh': user.token()['refresh_token'],
            "user_status": user.auth_status,
        }, status=200)


class ResetPasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ResetPasswordSerializer
    http_method_names = ['put', 'patch']

    def update(self, request, *args, **kwargs):
        response = super(ResetPasswordView, self).update(request, *args, **kwargs)
        try:
            user = User.objects.get(id=response.data.get['id'])
        except ObjectDoesNotExist:
            raise NotFound(detail='User not found')

        return Response({
            "success": True,
            'message': "Parol muvaffaqiyatli tiklandi",
            'access': user.token()['access'],
            'refresh': user.token()['refresh_token'],
        }, status=200)
