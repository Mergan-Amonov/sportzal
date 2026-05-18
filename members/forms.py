from django import forms
from .models import Member, Subscription, SubscriptionPlan

# Inline style for all dark-theme inputs
_INPUT_STYLE = (
    "width:100%; background:var(--bg); border:1px solid var(--border); color:var(--text);"
    "font-family:'Geist',sans-serif; font-size:13px; padding:9px 12px; border-radius:6px; outline:none;"
)
_SELECT_STYLE = _INPUT_STYLE + "cursor:pointer;"
_TEXTAREA_STYLE = _INPUT_STYLE + "resize:vertical;"


class MemberForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'style': _INPUT_STYLE}),
        required=False,
        label="Tug'ilgan sana"
    )

    class Meta:
        model = Member
        fields = ['full_name', 'phone', 'gender', 'birth_date', 'photo']
        widgets = {
            'full_name': forms.TextInput(attrs={'style': _INPUT_STYLE, 'placeholder': "Ism va familiya"}),
            'phone':     forms.TextInput(attrs={'style': _INPUT_STYLE, 'placeholder': "+998 90 123 45 67"}),
            'gender':    forms.Select(attrs={'style': _SELECT_STYLE}),
            'photo':     forms.FileInput(attrs={'style': _INPUT_STYLE}),
        }


class SubscriptionForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'style': _INPUT_STYLE}),
        label="Boshlanish sanasi"
    )

    class Meta:
        model = Subscription
        fields = ['plan', 'start_date', 'paid_amount', 'notes']
        widgets = {
            'plan':        forms.Select(attrs={'style': _SELECT_STYLE}),
            'paid_amount': forms.NumberInput(attrs={'style': _INPUT_STYLE, 'placeholder': "0"}),
            'notes':       forms.Textarea(attrs={'style': _TEXTAREA_STYLE, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].queryset = SubscriptionPlan.objects.all()
        self.fields['notes'].required = False


class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'duration_days', 'price', 'description']
        widgets = {
            'name':         forms.TextInput(attrs={'style': _INPUT_STYLE}),
            'duration_days': forms.NumberInput(attrs={'style': _INPUT_STYLE}),
            'price':        forms.NumberInput(attrs={'style': _INPUT_STYLE}),
            'description':  forms.Textarea(attrs={'style': _TEXTAREA_STYLE, 'rows': 2}),
        }
        labels = {
            'name': 'Nomi',
            'duration_days': 'Muddat (kun)',
            'price': "Narxi (so'm)",
            'description': 'Tavsif',
        }
