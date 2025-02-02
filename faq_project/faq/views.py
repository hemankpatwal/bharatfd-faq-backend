from rest_framework import viewsets
from .models import FAQ
from django.db import models
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from .serializers import FAQSerializer
from django.utils.translation import get_language
from django_filters import rest_framework as filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models.functions import Concat

class FAQFilter(filters.FilterSet):
    class Meta:
        model = FAQ
        fields = ['is_active', 'order']

def cache_page_with_lang(timeout):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            lang = request.query_params.get('lang', 'en')
            return cache_page(timeout, key_prefix=f'lang-{lang}')(view_func)(view_instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator

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
        language_code = self.request.query_params.get('lang', 'en')

        # Annotate the queryset with translated fields
        if language_code == 'en':
             # For English, use the base fields
            queryset = queryset.annotate(
                translated_question=F('question'),
                translated_answer=F('answer')
            )
        else:
            # For other languages, use the translated fields
            queryset = queryset.annotate(
                translated_question=F(f'question_{language_code}'),
                translated_answer=F(f'answer_{language_code}')
            )

        return queryset

def faq_preview(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    return render(request, 'faq/faq_preview.html', {'faq': faq})
