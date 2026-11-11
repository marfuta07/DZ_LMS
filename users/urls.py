from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentListAPIView, UserViewSet, UserRegisterAPIView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('register/', UserRegisterAPIView.as_view(), name='register'),
]