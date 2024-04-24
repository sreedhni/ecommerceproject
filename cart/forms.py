from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0 or rating > 5:
            raise forms.ValidationError("Rating must be between 0 and 5.")
        return rating