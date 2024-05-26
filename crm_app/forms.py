from django import forms
from .models import Complaint,CustomUser
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
class ComplaintForm(forms.ModelForm):
    # assigned_to = forms.ModelChoiceField(
    #     queryset=User.objects.filter(role='back_office'),
    #     required=False,
    #     widget=forms.Select,
    #     label='Assign to'
    # )
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(ComplaintForm, self).__init__(*args, **kwargs)
        if fields:
            allowed_fields = set(fields)
            existing_fields = set(self.fields.keys())
            for field in existing_fields - allowed_fields:
                self.fields.pop(field)

        if 'comments' in self.fields and self.initial.get('user_role') == 'operator':
            self.fields['comments'].widget.attrs['readonly'] = True
    class Meta:
        model = Complaint
        fields = ['client_account', 'client_name', 'client_phone', 'description', 'status',  'comments']
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'image']   