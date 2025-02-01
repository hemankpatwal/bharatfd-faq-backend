from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'question_hi', 'answer_hi', 'question_bn', 'answer_bn', 'is_active', 'order', 'created_at', 'updated_at']