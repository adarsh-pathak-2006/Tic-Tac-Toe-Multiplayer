from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import RegisterAPI, MyProfileAPI, ProfileAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('profile/me/', MyProfileAPI.as_view(), name='my_profile'),
    path('profile/all/', ProfileAPI.as_view(), name='all_profiles'),
]
