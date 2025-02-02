from django.contrib import admin
from .models import FAQ
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.translation import gettext_lazy as _


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'
        widgets = {
            'answer': CKEditorWidget(),
            'answer_hi': CKEditorWidget(),
            'answer_bn': CKEditorWidget(),
        }

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    form = FAQForm
    list_display = ('question', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question', 'question_hi', 'question_bn')
    list_editable = ('is_active', 'order')
    fieldsets = (
        (_('English Content'), {
            'fields': ('question', 'answer'),
        }),
        (_('Hindi Translation'), {
            'fields': ('question_hi', 'answer_hi'),
        }),
        (_('Bengali Translation'), {
            'fields': ('question_bn', 'answer_bn'),
        }),
        (_('Metadata'), {
            'fields': ('is_active', 'order'),
        }),
    )
    ordering = ('order', '-created_at')