from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter


class PaymentListAPIView(generics.ListAPIView):
    """Список платежей с фильтрацией и сортировкой."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter

    ordering_fields = ['payment_date']
    ordering = ['-payment_date']