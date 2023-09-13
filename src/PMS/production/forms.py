from datetime import datetime, timedelta
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.utils.translation import gettext_lazy as _
from production.models import Record


class ExportForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('record_dt',)

    record_dt = forms.DateField(label=_('record_date'))

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('record_dt', css_class='col-md-3'),
                Div(Submit('submit', _('export'), css_class='btn btn-info'),
                    css_class='col-md-3 d-flex align-items-center mt-3'),
                css_class='row'),
        )

        self.fields['record_dt'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )


class WoSearchForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('wo_no',)

    wo_no = forms.CharField(label=_('prod_order'))

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('wo_no', css_class='col-md-3'),
                Div(Submit('submit', _('search'), css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center mt-3'),
                css_class='row'),
        )


class RecordSearchForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('sap_emp_no', 'record_dt',)

    sap_emp_no = forms.CharField(required=True, label=_('sap_emp_no'))
    record_dt = forms.DateField(label=_('record_date'))

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('sap_emp_no', css_class='col-md-3'),
                Div('record_dt', css_class='col-md-3'),
                Div(Submit('submit', _('search'), css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center mt-3'),
                css_class='row'),
        )


        self.fields['record_dt'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('worked_labor_time', 'record_dt', 'plant', 'wo_no', 'item_no', 'spec', 'emp_no', 'username', 'sap_emp_no', 'step_code', 'step_name', 'cfm_code',
                  'labor_time', 'mach_time', 'good_qty', 'ng_qty', 'ctr_code', 'comment')

    record_dt = forms.DateField(label=_('record_date'))
    worked_labor_time = forms.DateField(required=False, label=_('worked_labor_time'))
    plant = forms.CharField(required=True, label=_('plant'))
    wo_no = forms.CharField(required=True, label=_('prod_order'))
    item_no = forms.CharField(required=True, label=_('item_no'))
    spec = forms.CharField(required=True, label=_('spec'))
    emp_no = forms.CharField(required=False, label=_('emp_no'))
    username = forms.CharField(required=False, label=_('name'))
    sap_emp_no = forms.CharField(required=True, label=_('sap_emp_no'))
    cfm_code = forms.CharField(required=True, label=_('confirm_code'))
    ctr_code = forms.CharField(required=True, label=_('control_code'))
    step_code = forms.CharField(required=False, label=_('step_code'))
    step_name = forms.CharField(required=False, label=_('step_name'), widget=forms.TextInput(attrs={'class': 'text-light bg-dark'}))
    labor_time = forms.CharField(required=True, label=_('labor_time'))
    mach_time = forms.CharField(required=False, label=_('mach_time'))
    good_qty = forms.IntegerField(required=True, label=_('good_qty'))
    ng_qty = forms.IntegerField(required=True, label=_('ng_qty'), initial=0)
    comment = forms.CharField(required=False, label=_('comment'), max_length=40)

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plant'].widget.attrs['readonly'] = True
        self.fields['wo_no'].widget.attrs['readonly'] = True
        self.fields['item_no'].widget.attrs['readonly'] = True
        self.fields['spec'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['emp_no'].widget.attrs['readonly'] = True
        self.fields['step_code'].widget.attrs['readonly'] = True
        self.fields['step_name'].widget.attrs['readonly'] = True
        self.fields['ctr_code'].widget.attrs['readonly'] = True
        self.fields['worked_labor_time'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('sap_emp_no', css_class='col-md-3'),
                Div('username', css_class='col-md-3'),
                Div('emp_no', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('record_dt', css_class='col-md-3'),
                Div('worked_labor_time', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('plant', css_class='col-md-3'),
                Div('wo_no', css_class='col-md-3'),
                Div('item_no', css_class='col-md-3'),
                Div('spec', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('cfm_code', css_class='col-md-3'),
                Div('step_code', css_class='col-md-3'),
                Div('step_name', css_class='col-md-3'),
                Div('ctr_code', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('good_qty', css_class='col-md-3'),
                Div('ng_qty', css_class='col-md-3'),
                Div('comment', css_class='col-md-6'),
                css_class='row'),
            Div(
                Div('mach_time', css_class='col-md-3'),
                Div('labor_time', css_class='col-md-3'),
                css_class='row'),
            Div(Submit('submit', _('save'), css_class='btn btn-info m-3'),
                css_class='row'),
        )


        self.fields['record_dt'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )


class RecordManageForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('record_dt',)

    record_dt = forms.DateField(label=_('record_date'))

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('record_dt', css_class='col-md-3'),
                Div(Submit('submit', _('search'), css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center mt-3'),
                css_class='row'),
        )


        self.fields['record_dt'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )
