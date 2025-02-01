from rest_framework import viewsets
from .models import FAQ
from .serializers import FAQSerializer
from django.utils.translation import get_language
from django_filters import rest_framework as filters

class FAQFilter(filters.FilterSet):
    class Meta:
        model = FAQ
        fields = ['is_active', 'order']

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.filter(is_active=True).order_by('order')
    serializer_class = FAQSerializer
    # filterset_class = FAQFilter

    def get_queryset(self):
        """
        Override the queryset to support language selection via ?lang= parameter.
        """
        queryset = super().get_queryset()
        lang = self.request.query_params.get('lang', get_language())

        # Annotate the queryset with translated fields
        for faq in queryset:
            faq.question = faq.get_question(lang)
            faq.answer = faq.get_answer(lang)
        return queryset