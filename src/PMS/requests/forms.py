from bootstrap_datepicker_plus import DateTimePickerInput
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from django.utils.translation import ugettext_lazy as _
from bases.models import Status
from projects.models import Project
from requests.models import Request, Level
from datetime import datetime

from users.models import CustomUser


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = (
        'title', 'start_date', 'due_date', 'process_rate', 'estimate_time', 'project', 'level', 'owner', 'desc',
        'belong_to', 'status', 'actual_date',)

    project = forms.ModelChoiceField(required=True, label=_('belong_project'), queryset=Project.objects.all())
    level = forms.ModelChoiceField(required=True, label=_('level'), queryset=Level.objects.all())
    title = forms.CharField(required=True, label=_('title'))
    desc = forms.CharField(required=False, label=_('desc'), widget=CKEditorUploadingWidget())
    status = forms.ModelChoiceField(required=True, label=_('status'), queryset=Status.objects.all())
    belong_to = forms.ModelChoiceField(required=False, label=_('belong'), queryset=None)
    owner = forms.ModelChoiceField(required=True, label=_('owner'), queryset=CustomUser.objects.all())
    estimate_time = forms.IntegerField(required=False, label=_('estimate_time'), widget=forms.NumberInput(), initial=0, )
    start_date = forms.DateField(label=_('starttime'), initial=datetime.now())
    due_date = forms.DateField(label=_('finishtime'), initial=datetime.now())
    actual_date = forms.DateField(required=False, label=_('actualtime'))

    def __init__(self, project, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.fields['belong_to'].queryset = Request.objects.filter(project=project).all()
        # if submit_title:
        #     self.helper.add_input(Submit('submit', submit_title))
        self.helper.layout = Layout(
            Div(Div('project', css_class='col-md-6'),
                Div('level', css_class='col-md-6'),
                css_class='row'),
            Div('title'),
            Div('desc'),
            Div('status'),
            Div('actual_date'),
            Div('belong_to'),
            Div(Div('owner', css_class='col-md-6'),
                Div('estimate_time', css_class='col-md-6'),
                css_class='row'),
            Div(Div('start_date', css_class='col-md-6'),
                Div('due_date', css_class='col-md-6'),
                css_class='row'),
        )

        self.fields['start_date'].widget = DateTimePickerInput(
            options={
                "format": "YYYY/MM/DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        ).start_of('request days')

        self.fields['due_date'].widget = DateTimePickerInput(
            options={
                "format": "YYYY/MM/DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        ).end_of('request days')

        self.fields['actual_date'].widget = DateTimePickerInput(
            options={
                "format": "YYYY/MM/DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )

    def clean_due_date(self):
        if self.cleaned_data['start_date'] <= self.cleaned_data['due_date']:
            return self.cleaned_data['due_date']
        else:
            raise forms.ValidationError(u"預計完成日期不能小於開始日期")
