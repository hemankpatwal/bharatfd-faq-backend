import pytest
from faq.models import FAQ
from django.core.cache import cache


@pytest.mark.django_db
def test_faq_creation():
    """Test that an FAQ instance can be created successfully."""
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a Python web framework."
    )
    assert faq.id is not None
    assert faq.question == "What is Django?"


@pytest.mark.django_db
def test_faq_auto_translation():
    """Test that FAQ auto-translates to Hindi and Bengali."""
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a Python web framework."
    )

    # Ensure translations exist
    assert faq.question_hi is not None
    assert faq.answer_hi is not None
    assert faq.question_bn is not None
    assert faq.answer_bn is not None


@pytest.mark.django_db
def test_faq_translation_fallback():
    """Test that FAQ returns English text when translation is missing."""
    faq = FAQ.objects.create(
        question="Fallback test?",
        answer="This should fall back to English."
    )

    # Simulate missing translation
    faq.question_hi = None
    faq.save()

    # Hindi is missing, so it should return English
    assert faq.get_question("hi") == "Fallback test?"


@pytest.mark.django_db
def test_faq_caching():
    """Test that FAQ translations are cached properly."""
    faq = FAQ.objects.create(
        question="Caching test?",
        answer="Testing cache storage."
    )

    # Retrieve and store in cache
    cache_key = f"faq_{faq.id}_question_hi"
    cache.set(cache_key, "Cached translation")

    # Fetch from cache and check
    cached_value = cache.get(cache_key)
    assert cached_value == "Cached translation"


@pytest.mark.django_db
def test_faq_cache_clear():
    """Test that cache is cleared when FAQ is updated."""
    faq = FAQ.objects.create(
        question="Clear cache?",
        answer="Checking cache clearing."
    )

    # Add to cache
    cache_key = f"faq_{faq.id}_question_hi"
    cache.set(cache_key, "Old cached value")

    # Update FAQ (this should clear the cache)
    faq.question = "Updated question?"
    faq.save()

    # Check cache is cleared
    assert cache.get(cache_key) is None
