from bootstrap_datepicker_plus import DateTimePickerInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from django.utils.translation import ugettext_lazy as _
from bases.models import Status
from requests.models import Request, Level
from datetime import datetime

from users.models import CustomUser


class RequestReceiveForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = (
            'start_date', 'due_date', 'estimate_time'
        )
        estimate_time = forms.IntegerField(required=False, label=_('estimate_time'), widget=forms.NumberInput(),
                                           initial=0, )
        start_date = forms.DateField(label=_('starttime'), initial=datetime.now(), input_formats=["%Y-%m-%d"])
        due_date = forms.DateField(label=_('finishtime'), initial=datetime.now(), input_formats=["%Y-%m-%d"])

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('start_date', css_class='col-md-6'),
                Div('due_date', css_class='col-md-6'),
                css_class='row'),
            Div('estimate_time'),
        )

        self.fields['start_date'].widget = DateTimePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        ).start_of('request days')

        self.fields['due_date'].widget = DateTimePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        ).end_of('request days')

    # def clean_due_date(self):
    #     if self.cleaned_data['start_date'] <= self.cleaned_data['due_date']:
    #         return self.cleaned_data['due_date']
    #     else:
    #         raise forms.ValidationError(u"預計完成日期不能小於開始日期")




class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = (
        'title', 'start_date', 'due_date', 'process_rate', 'estimate_time', 'level', 'owner', 'desc',
        'status', 'actual_date', 'is_test',)

    level = forms.ModelChoiceField(required=True, label=_('level'), queryset=Level.objects.all(), initial=2)
    title = forms.CharField(required=True, label=_('title'))
    desc = forms.CharField(required=False, label=_('desc'), widget=CKEditorUploadingWidget())
    status = forms.ModelChoiceField(required=True, label=_('status'), queryset=Status.objects.all(), initial=1)
    owner = forms.ModelChoiceField(required=False, label=_('owner'), queryset=CustomUser.objects.all())
    estimate_time = forms.IntegerField(required=False, label=_('estimate_time'), widget=forms.NumberInput(), initial=0, )
    start_date = forms.DateField(label=_('starttime'), initial=datetime.now(), input_formats=["%Y-%m-%d"])
    due_date = forms.DateField(label=_('finishtime'), initial=datetime.now(), input_formats=["%Y-%m-%d"])
    actual_date = forms.DateField(required=False, label=_('actualtime'), input_formats=["%Y-%m-%d"])
    is_test = forms.ChoiceField(label=_('need test'), choices=((False, 'False'), (True, 'True'),), required=False)

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('level', css_class='col-md-6'),
                Div('is_test', css_class='col-md-6'),
                css_class='row'),
            Div('title'),
            Div('desc'),
            Div('status'),
            Div('actual_date'),
            Div(Div('start_date', css_class='col-md-6'),
                Div('due_date', css_class='col-md-6'),
                css_class='row'),
            Div(Div('owner', css_class='col-md-6'),
                Div('estimate_time', css_class='col-md-6'),
                css_class='row'),
        )

        self.fields['start_date'].widget = DateTimePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        ).start_of('request days')

        self.fields['due_date'].widget = DateTimePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        ).end_of('request days')

        self.fields['actual_date'].widget = DateTimePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )

