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


# /////////////////////////////////// about me :>
from rest_framework import viewsets, permissions
from .models import Home, About, ResumeEntry, PortfolioItem, Service, ContactMessage, Skill
from .serializers import (
    HomeSerializer, AboutSerializer, ResumeEntrySerializer,
    PortfolioItemSerializer, ServiceSerializer, ContactMessageSerializer, SkillSerializer,ContactInfoSerializer, ContactInfo
)
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from rest_framework.permissions import SAFE_METHODS, BasePermission
from django.views.decorators.csrf import csrf_exempt
from .models import Home, About, ResumeEntry, PortfolioItem, Service

class ReadOnlyOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class HomeViewSet(viewsets.ModelViewSet):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    permission_classes = [ReadOnlyOrAdmin]

class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [ReadOnlyOrAdmin]

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = ResumeEntry.objects.all()
    serializer_class = ResumeEntrySerializer
    permission_classes = [ReadOnlyOrAdmin]

class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioItemSerializer
    permission_classes = [ReadOnlyOrAdmin]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [ReadOnlyOrAdmin]

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [ReadOnlyOrAdmin]

class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [ReadOnlyOrAdmin]  


# class ContactInfoViewSet(viewsets.ModelViewSet):
#     queryset = ContactInfo.objects.all()
#     serializer_class = ContactInfoSerializer
#     permission_classes = [ReadOnlyOrAdmin]



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def panel_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user and user.is_staff:
            login(request, user)
            return redirect('/panel/dashboard/')
        else:
            return render(request, 'admin_login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'admin_login.html')


@login_required
def panel_dashboard(request):
    return render(request, 'dashboard.html')


def index(request):
    # load singletons and lists for the public site
    home = Home.objects.first()
    about = About.objects.first()
    resume = ResumeEntry.objects.all().order_by('order', '-id')
    portfolio = PortfolioItem.objects.all()
    # ensure there's a portfolio card linking to API docs (swagger) so public site shows it
    try:
        if not portfolio.filter(details_url='/swagger/').exists():
            PortfolioItem.objects.create(title='API Documentation', category='Docs', description='API docs and playground', details_url='/swagger/')
            # requery to include the created item
            portfolio = PortfolioItem.objects.all()
    except Exception:
        # ignore creation errors at runtime
        portfolio = PortfolioItem.objects.all()
    services = Service.objects.all().order_by('-id')
    skills = Skill.objects.all().order_by('order', '-id')
    # fallbacks from defaults.py
    from . import defaults

    hero_roles = None
    if home and getattr(home, 'roles', None):
        hero_roles = home.roles
    else:
        hero_roles = defaults.HERO_ROLES

    about_desc = (about.description if about and getattr(about, 'description', None) else defaults.ABOUT_DESC)
    skills_desc = defaults.SKILLS_DESC
    resume_desc = defaults.RESUME_DESC
    portfolio_desc = defaults.PORTFOLIO_DESC
    services_desc = defaults.SERVICES_DESC

    # build safe portfolio items with resolved image URLs (avoid broken/missing media files)
    portfolio_items = []
    from django.conf import settings as _settings
    for p in portfolio:
        image_url = ''
        try:
            if getattr(p, 'image', None) and getattr(p.image, 'name', None):
                # accessing .url can raise ValueError if file is missing; guard it
                try:
                    image_url = p.image.url
                except Exception:
                    image_url = ''
        except Exception:
            image_url = ''
        portfolio_items.append({
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'details_url': p.details_url,
            'image_url': image_url,
            'category': p.category,
        })

    return render(request, 'index.html', {
        'home': home,
        'about': about,
        'resume_entries': resume,
        'portfolio_items': portfolio_items,
        'services': services,
        'skills': skills,
        'hero_roles': hero_roles,
        'about_desc': about_desc,
        'skills_desc': skills_desc,
        'resume_desc': resume_desc,
        'portfolio_desc': portfolio_desc,
        'services_desc': services_desc,
    })