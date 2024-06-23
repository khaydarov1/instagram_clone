from django.urls import path
from .views import CreateUserView,VerifyAPIView,GetNewVerification,ChangeUserInformationView
urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='create_user'),
    path('verify/', VerifyAPIView.as_view(), name='verify_user'),
    path('new-verify/', GetNewVerification, name='new_verify_user'),
    path('change-user/', ChangeUserInformationView.as_view(), name='change_user_information'),
]