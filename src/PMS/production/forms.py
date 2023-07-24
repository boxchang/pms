from datetime import datetime, timedelta
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from bootstrap_datepicker_plus.widgets import DatePickerInput

from production.models import Record


class WoSearchForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('wo_no',)

    wo_no = forms.CharField(label="工單")

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('wo_no', css_class='col-md-3'),
                Div(Submit('submit', '查詢', css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center mt-3'),
                css_class='row'),
        )


class RecordSearchForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('emp_no', 'record_dt',)

    emp_no = forms.CharField(required=True, label="員工編號")
    record_dt = forms.DateField(label="報工日期")

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('emp_no', css_class='col-md-3'),
                Div('record_dt', css_class='col-md-3'),
                Div(Submit('submit', '查詢', css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center mt-3'),
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
        fields = ('record_dt', 'plant', 'wo_no', 'spec', 'emp_no', 'username', 'sap_emp_no', 'step_code', 'step_name', 'cfm_code',
                  'labor_time', 'mach_time', 'good_qty', 'ng_qty', 'ctr_code')

    record_dt = forms.DateField(label="報工日期")
    plant = forms.CharField(required=True, label="工廠")
    wo_no = forms.CharField(required=True, label="工單")
    spec = forms.CharField(required=True, label="物料說明")
    emp_no = forms.CharField(required=True, label="員工編號")
    username = forms.CharField(required=False, label="姓名")
    sap_emp_no = forms.CharField(required=False, label="SAP員工編號")
    cfm_code = forms.CharField(required=True, label="確認碼")
    ctr_code = forms.CharField(required=True, label="確認碼")
    step_code = forms.CharField(required=False, label="站點代碼")
    step_name = forms.CharField(required=False, label="站點名稱")
    labor_time = forms.CharField(required=True, label="人時")
    mach_time = forms.CharField(required=False, label="機時")
    good_qty = forms.IntegerField(required=True, label="良品")
    ng_qty = forms.IntegerField(required=True, label="NG", initial=0)

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plant'].widget.attrs['readonly'] = True
        self.fields['wo_no'].widget.attrs['readonly'] = True
        self.fields['spec'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['sap_emp_no'].widget.attrs['readonly'] = True
        self.fields['step_code'].widget.attrs['readonly'] = True
        self.fields['step_name'].widget.attrs['readonly'] = True
        self.fields['ctr_code'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('emp_no', css_class='col-md-3'),
                Div('username', css_class='col-md-3'),
                Div('sap_emp_no', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('record_dt', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('plant', css_class='col-md-3'),
                Div('wo_no', css_class='col-md-3'),
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
                css_class='row'),
            Div(
                Div('mach_time', css_class='col-md-3'),
                Div('labor_time', css_class='col-md-3'),
                css_class='row'),
            Div(Submit('submit', '儲存', css_class='btn btn-info m-3'),
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

    record_dt = forms.DateField(label="報工日期")

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('record_dt', css_class='col-md-3'),
                Div(Submit('submit', '查詢', css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center mt-3'),
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
