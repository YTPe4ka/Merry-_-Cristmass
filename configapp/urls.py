from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import HomeViewSet, AboutViewSet, PortfolioViewSet, ServiceViewSet, ResumeViewSet, ContactViewSet

router = DefaultRouter()
router.register(r'home', HomeViewSet)
router.register(r'about', AboutViewSet)
router.register(r'portfolio', PortfolioViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'resume', ResumeViewSet)
router.register(r'contact', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
