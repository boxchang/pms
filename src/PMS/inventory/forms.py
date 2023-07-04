from datetime import datetime
from django import forms
from django.forms import modelformset_factory, inlineformset_factory, ModelForm

from .models import AppliedForm, ItemType, Item, AppliedItem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from bootstrap_datepicker_plus.widgets import DatePickerInput


# class OfficeItemForm(ModelForm):
#     class Meta:
#         model = AppliedItem
#         fields = '__all__'
        # widgets = {
        #     'item': forms.TextInput(
        #         attrs={
        #             'class': 'form-control'
        #         }
        #     ),
        #     'qty': forms.NumberInput(
        #         attrs={
        #             'class': 'form-control'
        #         }
        #     ),
        #     'price': forms.NumberInput(
        #         attrs={
        #             'class': 'form-control'
        #         }
        #     ),
        # }


ItemFormset = inlineformset_factory(AppliedForm, AppliedItem, fields=('item', 'price', 'qty'), extra=5, can_delete=True)


class OfficeInvForm(forms.ModelForm):
    class Meta:
        model = AppliedForm
        fields = ('unit', 'requester', 'apply_date', 'ext_number', 'reason')

        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    unit = forms.CharField(required=True, label="申請部門")
    requester = forms.CharField(required=True, label="申請人")
    apply_date = forms.CharField(required=True, label="申請日期")
    ext_number = forms.CharField(required=True, label="分機")
    type = forms.ModelChoiceField(required=False, label="物品種類", queryset=ItemType.objects.all())
    item = forms.ModelChoiceField(required=False, label="物品", queryset=Item.objects.all())
    item_qty = forms.IntegerField(required=False, label="數量")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('unit', css_class='col-md-4'),
                Div('requester', css_class='col-md-4'),
                Div('ext_number', css_class='col-md-4'),
                css_class='row'),
            Div(
                Div('apply_date', css_class='col-md-12'),
                css_class='row'),
            Div(
                Div('reason', css_class='col-md-12'),
                css_class='row'),
            Div(
                Div('type', css_class='col-md-4'),
                Div('item', css_class='col-md-4'),
                Div('item_qty', css_class='col-md-4'),
                css_class='row'),
        )

        self.fields['apply_date'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )
