from django import forms
from cheap_pints.models import Bar


class PintPriceForm(forms.ModelForm):
    """The form for handling new bar input"""
     
    barName = forms.CharField(help_text="Please enter the Bar Name.",
                             widget=forms.TextInput(attrs={'placeholder': 'Search and Select Bar'}),
                            max_length=Bar.NAME_MAX_LENGTH,
                           label="Bar Name:",
                           required=True)

    price = forms.FloatField(label="Pint Price:",
                                required=True)
    price_unit = forms.ChoiceField(initial=Bar.POUND,
                                                required=True,
                                                choices=Bar.PRICE_UNITS)


    googleId = forms.CharField(max_length=Bar.NAME_MAX_LENGTH, 
                                required=True,
                                widget=forms.HiddenInput)

    class Meta:
        model = Bar
        fields = ('barName','price', 'price_unit','googleId')