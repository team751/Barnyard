from django import forms

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
    component_group = forms.ChoiceField(choices=)

