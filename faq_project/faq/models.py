from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from deep_translator import GoogleTranslator

CACHE_TTL = 3600  # 1 hour


class FAQ(models.Model):
    # Base fields (English)
    question = models.TextField(_('Question (English)'))
    answer = RichTextField(_('Answer (English)'))

    # Hindi translations
    question_hi = models.TextField(
        _('Question (Hindi)'), blank=True, null=True)
    answer_hi = RichTextField(_('Answer (Hindi)'), blank=True, null=True)

    # Bengali translations
    question_bn = models.TextField(
        _('Question (Bengali)'), blank=True, null=True)
    answer_bn = RichTextField(_('Answer (Bengali)'), blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(
        default=0, help_text=_('Display order of the FAQ'))

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.question[:100]

    def get_translated_text(self, field_name, language_code):
        """
        Get the translated version of a field based on language code.
        Falls back to English if translation is not available.
        """
        if not self.pk:
            translated_field = f'{field_name}_{language_code}'
            translated_content = getattr(self, translated_field, None)
            return translated_content if translated_content else getattr(
                self, field_name)

        cache_key = f'faq_{self.id}_{field_name}_{language_code}'
        cached_value = cache.get(cache_key)

        if cached_value:
            return cached_value

        # Get the translated field if it exists
        translated_field = f'{field_name}_{language_code}'
        translated_content = getattr(self, translated_field, None)

        # Fallback to English if translation is not available
        content = translated_content if translated_content else getattr(
            self, field_name)

        # Cache the result for future requests
        cache.set(cache_key, content, timeout=CACHE_TTL)  # Cache for 1 hour

        return content

    def get_question(self, language_code):
        """Get the question in the specified language"""
        return self.get_translated_text('question', language_code)

    def get_answer(self, language_code):
        """Get the answer in the specified language"""
        return self.get_translated_text('answer', language_code)

    def clear_cache(self):
        """Clear all cached translations for this FAQ"""
        if not self.pk:
            return

        languages = ['en', 'hi', 'bn']
        fields = ['question', 'answer']

        for lang in languages:
            for field in fields:
                cache_key = f'faq_{self.id}_{field}_{lang}'
                cache.delete(cache_key)

    def translate_text(self, text, dest_language):
        """
        Translate text to the specified language using Google Translate.
        """
        try:
            translator = GoogleTranslator(source='en', target=dest_language)
            return translator.translate(text)
        except Exception as e:
            print(f"Translation error for {dest_language}: {e}")
            return text

    def auto_translate(self):
        """
        Automatically translate the question and answer into supported languages.
        """
        languages = {
            'hi': {'question': 'question_hi', 'answer': 'answer_hi'},
            'bn': {'question': 'question_bn', 'answer': 'answer_bn'},
            # Add more languages here
        }

        for language_code, fields in languages.items():
            if not getattr(
                    self,
                    fields['question']) or not getattr(
                    self,
                    fields['answer']):
                # Translate question
                translated_question = self.translate_text(
                    self.question, language_code)
                if translated_question:
                    setattr(self, fields['question'], translated_question)

                # Translate answer
                translated_answer = self.translate_text(
                    self.answer, language_code)
                if translated_answer:
                    setattr(self, fields['answer'], translated_answer)

    def save(self, *args, **kwargs):
        """
        Override save to auto-translate FAQs before saving.
        """
        # For new instances or when specific fields are updated
        update_fields = kwargs.get('update_fields', [])
        needs_translation = (
            not self.pk) or (
            'question' in update_fields) or (
            'answer' in update_fields)

        if needs_translation:
            self.auto_translate()

        # Clear cache for existing instances
        if self.pk:
            self.clear_cache()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Override delete to clear cache when FAQ is deleted.
        """
        super().delete(*args, **kwargs)
        self.clear_cache()
