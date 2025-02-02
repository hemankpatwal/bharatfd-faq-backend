from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'question_hi', 'answer_hi', 'question_bn', 'answer_bn', 'is_active', 'order', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["question"] = data.pop('translated_question', data.get('question'))
        data["answer"] = data.pop('translated_answer', data.get('answer'))

        return data