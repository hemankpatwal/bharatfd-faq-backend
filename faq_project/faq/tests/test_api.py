import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from faq.models import FAQ


@pytest.mark.django_db
class TestFAQAPI:
    def setup_method(self):
        self.client = APIClient()
        self.faq_data = {
            'question': 'What is Django?',
            'answer': 'Django is a high-level Python web framework.',
            'question_hi': 'Django क्या है?',
            'answer_hi': 'Django एक उच्च-स्तरीय Python वेब फ्रेमवर्क है।',
            'question_bn': 'Django কি?',
            'answer_bn': 'Django হল একটি উচ্চ-স্তরের Python ওয়েব ফ্রেমওয়ার্ক।',
            'is_active': True,
            'order': 1,
        }
        self.faq = FAQ.objects.create(**self.faq_data)

    def test_get_faq_list(self):
        url = reverse('faq-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_get_faq_detail(self):
        url = reverse('faq-detail', args=[self.faq.id])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['question'] == self.faq_data['question']

    def test_create_faq(self):
        url = reverse('faq-list')
        new_faq_data = {
            'question': 'What is REST?',
            'answer': 'REST is an architectural style for designing networked applications.',
            'is_active': True,
            'order': 2,
        }
        response = self.client.post(url, new_faq_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert FAQ.objects.filter(question=new_faq_data['question']).exists()

    def test_update_faq(self):
        url = reverse('faq-detail', args=[self.faq.id])
        updated_data = {'question': 'What is Django REST Framework?'}
        response = self.client.patch(url, updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.faq.refresh_from_db()
        assert self.faq.question == updated_data['question']

    def test_delete_faq(self):
        url = reverse('faq-detail', args=[self.faq.id])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not FAQ.objects.filter(id=self.faq.id).exists()

    def test_language_selection(self):
        url = reverse('faq-list')
        response = self.client.get(url, {'lang': 'hi'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['question'] == self.faq_data['question_hi']
