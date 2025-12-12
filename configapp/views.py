# # from rest_framework import generics
# # from .models import Category, Product, Supplier
# # from .serializers import CategorySerializer, ProductSerializer, SupplierSerializer

# # class CategoryListCreate(generics.ListCreateAPIView):
# #     queryset = Category.objects.all()
# #     serializer_class = CategorySerializer

# # class SupplierListCreate(generics.ListCreateAPIView):
# #     queryset = Supplier.objects.all()
# #     serializer_class = SupplierSerializer

# # class ProductListCreate(generics.ListCreateAPIView):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from drf_yasg.utils import swagger_auto_schema
# from .models import Category, Product, Supplier
# from .serializers import CategorySerializer, ProductSerializer, SupplierSerializer


# class CategoryApi(APIView):

#     @swagger_auto_schema(
#         responses={200: CategorySerializer(many=True)}
#     )
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         request_body=CategorySerializer,
#         responses={201: CategorySerializer}
#     )
#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class ProductApi(APIView):

#     @swagger_auto_schema(
#         responses={200: ProductSerializer(many=True)}
#     )
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         request_body=ProductSerializer,
#         responses={201: ProductSerializer}
#     )
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# class SupplierApi(APIView):

#     @swagger_auto_schema(
#         responses={200: SupplierSerializer(many=True)}
#     )
#     def get(self, request):
#         suppliers = Supplier.objects.all()
#         serializer = SupplierSerializer(suppliers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         request_body=SupplierSerializer,
#         responses={201: SupplierSerializer}
#     )
#     def post(self, request):
#         serializer = SupplierSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









from django.conf import settings
from django.core.cache import cache
import random
import threading
from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Category, Supplier, Product, Todo
from .serializers import CategorySerializer, SupplierSerializer, ProductSerializer ,EmailRegisterserializer, TodoSerializer,UserRegisterSerializer,EmailVerifySerializer,LoginSerializer,SendEmailSerializer
from django.contrib.auth import  *
from django.contrib.auth.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status
from rest_framework import permissions
from django.core.mail import send_mail
from django.conf import settings
# Category
class CategoryApi(APIView):
    @swagger_auto_schema(responses={200: CategorySerializer(many=True)})
    def get(self, request):
        qs = Category.objects.all()
        return Response(CategorySerializer(qs, many=True).data)

    @swagger_auto_schema(request_body=CategorySerializer, responses={201: CategorySerializer})
    def post(self, request):
        s = CategorySerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailApi(APIView):
    @swagger_auto_schema(responses={200: CategorySerializer})
    def get(self, request, pk):
        try:
            obj = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(CategorySerializer(obj).data)

    @swagger_auto_schema(request_body=CategorySerializer, responses={200: CategorySerializer})
    def put(self, request, pk):
        try:
            obj = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = CategorySerializer(obj, data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Supplier
class SupplierApi(APIView):
    @swagger_auto_schema(responses={200: SupplierSerializer(many=True)})
    def get(self, request):
        qs = Supplier.objects.all()
        return Response(SupplierSerializer(qs, many=True).data)

    @swagger_auto_schema(request_body=SupplierSerializer, responses={201: SupplierSerializer})
    def post(self, request):
        s = SupplierSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class SupplierDetailApi(APIView):
    @swagger_auto_schema(responses={200: SupplierSerializer})
    def get(self, request, pk):
        try:
            obj = Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(SupplierSerializer(obj).data)

    @swagger_auto_schema(request_body=SupplierSerializer, responses={200: SupplierSerializer})
    def put(self, request, pk):
        try:
            obj = Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = SupplierSerializer(obj, data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Product
class ProductApi(APIView):
    @swagger_auto_schema(responses={200: ProductSerializer(many=True)})
    def get(self, request):
        qs = Product.objects.all()
        return Response(ProductSerializer(qs, many=True).data)

    @swagger_auto_schema(request_body=ProductSerializer, responses={201: ProductSerializer})
    def post(self, request):
        s = ProductSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailApi(APIView):
    @swagger_auto_schema(responses={200: ProductSerializer})
    def get(self, request, pk):
        try:
            obj = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(obj).data)

    @swagger_auto_schema(request_body=ProductSerializer, responses={200: ProductSerializer})
    def put(self, request, pk):
        try:
            obj = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = ProductSerializer(obj, data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CustomUserManage(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(username, password, **extra_fields)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        
        return self.create_user(username, password, **extra_fields)
    


def get_tokens_for_user(User):
    refresh = RefreshToken.for_user(User)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class EmailRegister(APIView):
    @swagger_auto_schema(request_body=EmailRegisterserializer, responses={200: "Verification code sent to email"},operation_description="Register with email to receive a verification code.")


    def post(self, request):
        serializer= EmailRegisterserializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        code = random.randint(1000, 9999)
        cache.set(f'otp_{email}', code, timeout=300)
        print(f"Verification code for {email}: {code}")  # For testing purposes
        # th =  threading.Thread(target=send_email_code, args=(email, code))
        # th.start()  
        return Response({"message": "Verification code sent to email"}, status=status.HTTP_200_OK)


class EmailVerify(APIView):
    @swagger_auto_schema(request_body=EmailVerifySerializer, responses={200: "Email verified successfully"},operation_description="Verify the email with the received code.")
    def post(self, request):
        serializer= EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = request.data.get('code')

        cached_code = cache.get(f'otp_{email}')
        if cached_code and str(cached_code) == str(code):
            cache.set(f'verify_{email}', True, timeout=600)  # Mark email as verified for 10 minutes
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired verification code"}, status=status.HTTP_400_BAD_REQUEST)

class UserRegister(APIView):
    # parser_classes=(MultiPartParser, FormParser)
    @swagger_auto_schema(request_body=UserRegisterSerializer, responses={201: UserRegisterSerializer},operation_description="Register a new user with username and password.")
    def post(self, request):
        serializer= UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            result = cache.get(f'verify_{email}')
            if result:
                serializer.save(is_active=True)
                tokens = get_tokens_for_user(User)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Email not verified"}, status=status.HTTP_400_BAD_REQUEST)
            
        else:   
            return Response(serializer.data, status=status.HTTP_201_CREATED)

#////////////////////////////////
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        tokens = get_tokens_for_user(user)

        return Response({
            "status": True,
            "message": "Login muvaffaqiyatli",
            "tokens": tokens,
            "user": {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "is_user": user.is_user
            }
        }, status=status.HTTP_200_OK)
# ////////////////////////////////////////








    
# class TodoViewSet(viewsets.ModelViewSet):
#     serializer_class = TodoSerializer
#     permission_classes = [IsAuthenticated] 








class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class SendEmailApi(APIView):
    @swagger_auto_schema(request_body=SendEmailSerializer, responses={200: "Verification code sent to email"},operation_description="Send a verification code to the provided email.")
    def post(self, request):
        subject ='Test Email pernol'
        message = request.data.get('text')
        email = request.data.get('email')
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [f"{email}"] 
        send_mail( subject, message, email_from, recipient_list )
        return Response(data =f"{email}", status=status.HTTP_200_OK)
    









 # qfxn wglj vtri lply
# qfxn wglj vtri lply
# qfxn wglj vtri lply
# qfxn wglj vtri lply
# qfxn wglj vtri lply
# qfxn wglj vtri lply
# qfxn wglj vtri lply
# qfxn wglj vtri lply
# qfxn wglj vtri lply
