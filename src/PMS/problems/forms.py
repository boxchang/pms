from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Button
from django import forms
from datetime import datetime, timedelta
from bases.models import Status
from problems.models import Problem, Problem_reply, ProblemType
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus.widgets import DatePickerInput


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('problem_type', 'problem_status', 'title', 'desc')

    problem_type = forms.ModelChoiceField(required=False, label="問題類型", queryset=ProblemType.objects.all(), initial=1)
    problem_status = forms.ModelChoiceField(required=False, label="問題狀態", queryset=Status.objects.all(), initial=1)
    title = forms.CharField(required=True, label=_('title'))
    desc = forms.CharField(required=False, label=_('desc'), widget=CKEditorUploadingWidget())

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Div(
                Div('problem_type', css_class='col-md-3'),
                Div('problem_status', css_class='col-md-3'),
                Div('title', css_class='col-md-6'),
                css_class='row'),
            Div('desc'),
        )


class ProblemReplyForm(forms.ModelForm):
    class Meta:
        model = Problem_reply
        fields = ('comment', )

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

    comment = forms.CharField(
        required=True, label='', widget=CKEditorUploadingWidget())


class ProblemHistoryForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('status', 'start_date', 'due_date',)

    status = forms.ModelChoiceField(required=False, label=_(
        'status'), queryset=Status.objects.all(), initial=1)
    start_date = forms.DateField(label="建立日期(起)")
    due_date = forms.DateField(label="建立日期(迄)")

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
                attrs={'value': (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d')},
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

class ProblemChartForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('status', 'start_date',)

    status = forms.ModelChoiceField(required=False, label=_(
        'status'), queryset=Status.objects.all(), initial=1)
    start_date = forms.DateField(label="建立日期(起)")

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('start_date', css_class='col-md-3'),
                Div('status', css_class='col-md-3'),
                Div(Button('search', '查詢', css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center search_btn_fix'),
                css_class='row'),
        )

        self.fields['start_date'].widget = DatePickerInput(
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
                options={
                    "format": "YYYY-MM",
                    "showClose": False,
                    "showClear": False,
                    "showTodayButton": False,
                }
            )
