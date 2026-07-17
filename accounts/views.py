# from rest_framework.authtoken.models import Token
# from accounts.serializers import SignUpSerializer, LoginSerializer, UserSerializer, ResetPasswordEmail, SetNewPasswordSerializer
# from django.utils.timezone import now
# from rest_framework import status
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.viewsets import ModelViewSet

# from accounts.models import CustomUser
# from accounts.utils import EmailService

# class UsersView(ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = CustomUser.objects.all()
#     permission_classes = (IsAuthenticated, )

# # Sign Up View
# class SignUpView(APIView):
#     def post(self, request):
#         serializer = SignUpSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key, 'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Login View
# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key, 'message': 'Login successful!'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CustomForgetPasswordView(APIView):
#     serializer_class = ResetPasswordEmail
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             user = User.objects.filter(email=email).first()

#             if user:
#                 EmailService().send_email(email, user.user_uuid)
#                 return Response({"message": "success"}, status=200)
#             else:
#                 return Response({"message": "success"}, status=200)
#         else:
#             return Response(serializer.errors)
        
# class SetNewPasswordView(APIView):
#     serializer_class = SetNewPasswordSerializer
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         current_time = now().timestamp()
#         if serializer.is_valid():
#             try:
#                 user = User.objects.filter(user_uuid=serializer.validated_data['uuid']).first()
#             except:
#                 return Response({"message": "token is incorrect"})
#             try:
#                 check_expiry = serializer.validated_data['expiry']
#                 if float(current_time) > float(check_expiry):
#                     return Response({"message": "This link has been expired"}, status=400)
#             except:
#                 pass
#             if user:
#                 new_password = serializer.validated_data['new_password']
#                 user.set_password(new_password)
#                 user.is_active = True
#                 user.save()
#                 EmailService().password_reset_confirm(user, "Password reset successful")
#                 return Response({"message": "success", }, status=200)
#             return Response({"message": "token not valid", }, status=400)
#         else:
#             return Response(serializer.errors)

from rest_framework.authtoken.models import Token
from accounts.serializers import (
    SignUpSerializer, LoginSerializer, UserSerializer, ResetPasswordEmail, SetNewPasswordSerializer, ProfileSerializer
)
from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from accounts.models import CustomUser
from accounts.utils import EmailService
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        print("Serialized User Data:", serializer.data)  # Debugging
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        data = request.data.copy()
        data.pop("email", None)  # Prevent email update
        data.pop("password", None)  # Prevent password update

        serializer = ProfileSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UsersView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, )

# Sign Up View
class SignUpView(APIView):
    @swagger_auto_schema(
        request_body=SignUpSerializer,
        responses={201: openapi.Response("User registered successfully")},
    )
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: openapi.Response("Login successful!")},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data  # Get user and role
            user = user_data["user"]
            role = user_data["role"]

            token, _ = Token.objects.get_or_create(user=user)
            
            print(token.key)  # Debugging: Print the token key

            # Return token and role
            return Response({
                'token': token.key,
                'role': role,  # Include the role
                'message': 'Login successful!',
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomForgetPasswordView(APIView):
    serializer_class = ResetPasswordEmail
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ResetPasswordEmail,
        responses={200: openapi.Response("Success")},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()

            if user:
                EmailService().send_email(email, user.user_uuid)
            return Response({"message": "success"}, status=200)
        return Response(serializer.errors)

class SetNewPasswordView(APIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SetNewPasswordSerializer,
        responses={200: openapi.Response("Password reset successful")},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        current_time = now().timestamp()
        if serializer.is_valid():
            user = CustomUser.objects.filter(user_uuid=serializer.validated_data['uuid']).first()
            if not user:
                return Response({"message": "token is incorrect"}, status=400)

            check_expiry = serializer.validated_data.get('expiry')
            if check_expiry and float(current_time) > float(check_expiry):
                return Response({"message": "This link has been expired"}, status=400)

            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.is_active = True
            user.save()
            EmailService().password_reset_confirm(user, "Password reset successful")
            return Response({"message": "success"}, status=200)

        return Response(serializer.errors)
