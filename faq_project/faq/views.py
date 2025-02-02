from rest_framework import viewsets
from .models import FAQ
from django.shortcuts import render, get_object_or_404
from .serializers import FAQSerializer
from django.utils.translation import get_language
from django_filters import rest_framework as filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class FAQFilter(filters.FilterSet):
    class Meta:
        model = FAQ
        fields = ['is_active', 'order']

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.filter(is_active=True).order_by('order')
    serializer_class = FAQSerializer

    @method_decorator(cache_page(60 * 15))  # Cache API responses for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))  # Cache API responses for 15 minutes
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        """
        Override the queryset to support language selection via ?lang= parameter.
        """
        queryset = super().get_queryset()
        lang = self.request.query_params.get('lang', 'en')

        # Annotate the queryset with translated fields
        for faq in queryset:
            faq.question = faq.get_question(lang)
            faq.answer = faq.get_answer(lang)
        return queryset


def faq_preview(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    return render(request, 'faq/faq_preview.html', {'faq': faq})
