from datetime import datetime

from django import forms
from .models import Borrow, BPMDept, BPMUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Fieldset
from bootstrap_datepicker_plus.widgets import DatePickerInput


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = (
            'apply_date', 'expect_date', 'comment')

    comment = forms.CharField(required=True, label="借用原因")
    apply_date = forms.CharField(required=True, label="借用日期", initial=datetime.strftime(datetime.now(), "%Y-%m-%d"))
    expect_date = forms.CharField(required=True, label="預計歸還日期", initial=datetime.strftime(datetime.now(), "%Y-%m-%d"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('apply_date', css_class='col-md-6'),
                Div('expect_date', css_class='col-md-6'),
                css_class='row'),
            Div(
                Div('comment', css_class='col-md-12'),
                css_class='row'),
        )

        self.fields['apply_date'].widget = DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )

        self.fields['expect_date'].widget = DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )

class BorrowModifiedForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = (
            'lend_date', 'return_date', 'admin_comment')
