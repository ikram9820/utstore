from django import forms

from store.models import Order

PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(coerce=int,initial=1, choices=PRODUCT_QUANTITY_CHOICES)
    override = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
        'postal_code', 'city']

class SearchForm(forms.Form):
    query = forms.CharField()