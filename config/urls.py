# """
# URL configuration for config project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# # from django.urls import path
# # from django.contrib import admin
# # from configapp.views import CategoryListCreate, SupplierListCreate, ProductListCreate

# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# #     path('categories/', CategoryListCreate.as_view()),
# #     path('suppliers/', SupplierListCreate.as_view()),
# #     path('products/', ProductListCreate.as_view()),
# # ]


# # from django.contrib import admin
# # from django.urls import path, include
# # from drf_yasg.views import get_schema_view
# # from drf_yasg import openapi
# # from rest_framework import permissions

# # schema_view = get_schema_view(
# #    openapi.Info(
# #       title="API docs",
# #       default_version='v1',
# #       description="API documentation",
# #    ),
# #    public=True,
# #    permission_classes=(permissions.AllowAny,),
# # )
# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# #     path('categories/', include('configapp.urls')),  
# #     path('suppliers/', include('configapp.urls')),   
# #     path('products/', include('configapp.urls')),    

# #     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
# #     path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
# #     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# # ]

# from django.contrib import admin
# from django.urls import path
# from django.urls import re_path
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from rest_framework import permissions
# from configapp.views import OrderDetailApi,OrderApi


# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

# urlpatterns = [
#     path('admin/', admin.site.urls),
#    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('orders/', OrderApi.as_view(), name='orders'),
#     path('orders/<int:pk>/', OrderDetailApi.as_view(), name='order-detail'),
# ]








from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from configapp import views as app_views
from configapp.views import (
    CategoryApi, CategoryDetailApi,
    SupplierApi, SupplierDetailApi,
    ProductApi, ProductDetailApi,
    EmailRegister, EmailVerify, SendEmailApi,
    UserRegister, LoginView,
    TodoViewSet,
)

# ================== SWAGGER ==================
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="API docs",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ================== ROUTER ==================
router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')
# register internal viewsets for public content editable via dashboard
router.register(r'home', app_views.HomeViewSet, basename='home')
router.register(r'about', app_views.AboutViewSet, basename='about')
router.register(r'resume', app_views.ResumeViewSet, basename='resume')
router.register(r'portfolio', app_views.PortfolioViewSet, basename='portfolio')
router.register(r'services', app_views.ServiceViewSet, basename='services')
router.register(r'skills', app_views.SkillViewSet, basename='skills')
router.register(r'contact', app_views.ContactViewSet, basename='contact')

# ================== URLS ==================
urlpatterns = [

    # ===== API =====
    path('api/', include(router.urls)),
    path('api/categories/', CategoryApi.as_view()),
    path('api/categories/<int:pk>/', CategoryDetailApi.as_view()),
    path('api/suppliers/', SupplierApi.as_view()),
    path('api/suppliers/<int:pk>/', SupplierDetailApi.as_view()),
    path('api/products/', ProductApi.as_view()),
    path('api/products/<int:pk>/', ProductDetailApi.as_view()),

    # ===== AUTH =====
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),

    path('api/register/', UserRegister.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/email/', EmailRegister.as_view()),
    path('api/confirmemail/', EmailVerify.as_view()),
    path('api/sendemail/', SendEmailApi.as_view()),

    # ===== CUSTOM ADMIN =====
    path('panel/login/', app_views.panel_login, name='panel-login'),
    path('panel/dashboard/', app_views.panel_dashboard, name='panel-dashboard'),

    # ===== SWAGGER =====
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),

    # ===== SITE =====
    path('', app_views.index, name='home'),
    # Django admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# # app1/urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import PhoneRegister, PhoneConfirm, UserRegister, LoginView, TodoViewSet

# urlpatterns = [
#     path("phone/", PhoneRegister.as_view(), name="phone-register"),
#     path("confirmphone/", PhoneConfirm.as_view(), name="phone-confirm"),
#     path("register/", UserRegister.as_view(), name="user-register"),
#     path("login/", LoginView.as_view(), name="login"),
#     path("", include(router.urls)),
# ]