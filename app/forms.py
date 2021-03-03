from django.contrib.auth.models import User
from django.forms import ModelForm

from app.models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('stars', 'text')
        labels = {
            'stars': 'Оценка',
            'text': 'Отзыв'
        }
