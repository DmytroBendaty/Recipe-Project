from django import forms


class RatingForm(forms.Form):
    RATING_CHOICES = [
        (1, '1 зірка'),
        (2, '2 зірки'),
        (3, '3 зірки'),
        (4, '4 зірки'),
        (5, '5 зірок'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES, widget=forms.RadioSelect)
