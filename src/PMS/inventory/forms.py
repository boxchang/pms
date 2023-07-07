from datetime import datetime, timedelta
from django import forms
from django.forms import modelformset_factory, inlineformset_factory, ModelForm

from users.models import Unit, CustomUser
from .models import AppliedForm, ItemType, Item, AppliedItem, ItemCategory, FormStatus
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Button, Submit
from bootstrap_datepicker_plus.widgets import DatePickerInput

class InvAppliedHistoryForm(forms.ModelForm):
    class Meta:
        model = AppliedForm
        fields = ('status', 'start_date', 'due_date',)

    status = forms.ModelChoiceField(required=False, label="狀態", queryset=FormStatus.objects.all(), initial=0)
    start_date = forms.DateField(label="申請日期(起)")
    due_date = forms.DateField(label="申請日期(迄)")

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('start_date', css_class='col-md-3'),
                Div('due_date', css_class='col-md-3'),
                Div('status', css_class='col-md-3'),
                Div(Submit('submit', '查詢', css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center'),
                css_class='row'),
        )

        self.fields['start_date'].widget = DatePickerInput(
            attrs={'value': (datetime.now()-timedelta(days=45)).strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )

        self.fields['due_date'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )


class OfficeInvForm(forms.ModelForm):
    class Meta:
        model = AppliedForm
        fields = ('unit', 'requester', 'apply_date', 'ext_number', 'reason')

    reason = forms.CharField(required=True, label="原因", widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))
    unit = forms.ModelChoiceField(required=True, label="申請部門", queryset=Unit.objects.all(), widget=forms.Select(attrs={"onChange": "dept_change()"}))
    requester = forms.ModelChoiceField(required=True, label="申請人", queryset=CustomUser.objects.none())
    apply_date = forms.CharField(required=True, label="申請日期")
    ext_number = forms.CharField(required=False, label="分機")
    category = forms.ModelChoiceField(required=False, label="物品類別", queryset=ItemCategory.objects.all())
    type = forms.ModelChoiceField(required=False, label="物品種類", queryset=ItemType.objects.all())
    item = forms.ModelChoiceField(required=False, label="物品", queryset=Item.objects.all())
    item_qty = forms.IntegerField(required=False, label="數量")
    keyword = forms.CharField(required=False, label="關鍵字")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('unit', css_class='col-md-3'),
                Div('requester', css_class='col-md-3'),
                Div('ext_number', css_class='col-md-3'),
                Div('apply_date', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('reason', css_class='col-md-12'),
                css_class='row'),
            Div(
                Div('category', css_class='col-md-2'),
                Div('type', css_class='col-md-2'),
                Div('keyword', css_class='col-md-2'),
                Div(Button('search', '查詢', css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center search_btn_fix'),
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
