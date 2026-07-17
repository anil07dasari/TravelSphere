from django.urls import path
from .views import SignUpView, LoginView, UsersView, CustomForgetPasswordView, SetNewPasswordView, UserProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/profile/', UserProfileView.as_view(), name='profile'),
    path('users/', UsersView.as_view({"get": "list"})),
    path('users/<int:pk>/', UsersView.as_view({"get": "retrieve", "delete": "destroy"})),
    path('password_reset/', CustomForgetPasswordView.as_view()),
    path('password_reset/confirm/', SetNewPasswordView.as_view()),
]
