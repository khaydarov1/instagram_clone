from django.urls import path
from .views import CreateUserView, VerifyAPIView, GetNewVerification, \
    ChangeUserInformationView, ChangeUserPhotoView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', CreateUserView.as_view(), name='create_user'),
    path('verify/', VerifyAPIView.as_view(), name='verify_user'),
    path('new-verify/', GetNewVerification.as_view(), name='new_verify_user'),
    path('change-user/', ChangeUserInformationView.as_view(), name='change_user_information'),
    path('change-user-photo/', ChangeUserPhotoView.as_view(), name='change_user_photo'),

]
