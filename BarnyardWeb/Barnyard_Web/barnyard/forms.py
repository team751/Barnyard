from django import forms

from Barnyard_Web.barnyard.sheets.utils import get_component_groups


class ItemForm(forms.Form):
    name = forms.CharField(help_text="Name",
                           required=True,
                           widget=forms.TextInput())
    description = forms.CharField(help_text="Description",
                                  required=True,
                                  widget=forms.TextInput())
    location = forms.CharField(help_text="Location",
                               required=True,
                               widget=forms.TextInput())
    image_url = forms.CharField(help_text="Image URL",
                                required=True,
                                widget=forms.TextInput())
    component_group = forms.ChoiceField(help_text="Component Group",
                                        choices=get_component_groups(),
                                        required=True)

    price = forms.DecimalField(help_text="Price per Item(BOM)", min_value=0, required=False)
    quantity = forms.IntegerField(help_text="Quantity(BOM)", min_value=1, required=False)
    on_robot = forms.BooleanField(help_text="On Robot(BOM)", required=False)
    exempt = forms.BooleanField(help_text="Exempt(BOM)", required=False)
    asap = forms.BooleanField(help_text="ASAP?(BOM)", required=False)
    order_link = forms.CharField(help_text="Order Link(BOM)", required=False)
