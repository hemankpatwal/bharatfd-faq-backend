from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FAQViewSet, faq_preview 

router = DefaultRouter()
router.register(r'faqs', FAQViewSet, basename='faq')

urlpatterns = [
    path('', include(router.urls)),
    path('preview/<int:pk>/', faq_preview, name='faq-preview'),
]