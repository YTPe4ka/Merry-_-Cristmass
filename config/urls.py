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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenVerifyView

from configapp.views import (
    CategoryApi, CategoryDetailApi, EmailRegister, SendEmailApi,
    SupplierApi, SupplierDetailApi,
    ProductApi, ProductDetailApi, UserRegister,EmailVerify
)
from configapp.views import TodoViewSet, LoginView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="API docs",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)




router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')



urlpatterns = [
    path('admin/', admin.site.urls),

    # swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # api
    path('categories/', CategoryApi.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailApi.as_view(), name='category-detail'),
    path('suppliers/', SupplierApi.as_view(), name='suppliers'),
    path('suppliers/<int:pk>/', SupplierDetailApi.as_view(), name='supplier-detail'),
    path('products/', ProductApi.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailApi.as_view(), name='product-detail'),
    # token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # register
    path("email/",EmailRegister.as_view()),
    path("confirmemail/",EmailVerify.as_view()),
    path("register",UserRegister.as_view()),
    path("login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
    # todoits 

    #email
    path("sendemail/",SendEmailApi.as_view()),
    

]
    







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