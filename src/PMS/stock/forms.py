from datetime import datetime, timedelta

from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Button, Submit, HTML

from stock.models import Storage, Location, Bin


class WoSearchForm(forms.Form):
    wo_no = forms.CharField(required=True, label="工單號碼")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('wo_no', css_class='col-md-8'),
                Div(Submit('search', '查詢', css_class='btn btn-info'),
                    css_class='col-md-2 d-flex align-items-center search_btn_fix pt-3'),
                css_class='row'),
        )


class SearchForm(forms.Form):
    wo_no = forms.CharField(required=False, label="工單號碼")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('wo_no', css_class='col-md-8'),
                Div(Submit('search', '查詢', css_class='btn btn-info'),
                    css_class='col-md-2 d-flex align-items-center search_btn_fix pt-3'),
                css_class='row'),
        )


# 有Bin
class StockForm(forms.Form):
    storage = forms.ModelChoiceField(required=False, label="Storage", queryset=Storage.objects.all())
    location = forms.ModelChoiceField(required=False, label="Location", queryset=Location.objects.all())
    bin = forms.CharField(max_length=20, label="Bin儲格", required=True)
    desc = forms.CharField(max_length=50, label="備註", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('storage', css_class='col-md-4'),
                Div('location', css_class='col-md-4'),
                Div('bin', css_class='col-md-4'),
                css_class='row'),
            Div(
                Div('desc', css_class='col-md-12'),
                css_class='row'),
        )


# 無Bin
class StockForm2(forms.Form):
    storage = forms.ModelChoiceField(required=False, label="Storage", queryset=Storage.objects.all())
    location = forms.ModelChoiceField(required=False, label="Location", queryset=Location.objects.none())
    bin = forms.ModelChoiceField(required=False, label="Bin儲格", queryset=Bin.objects.none())
    desc = forms.CharField(max_length=50, label="備註", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('storage', css_class='col-md-4'),
                Div('location', css_class='col-md-4'),
                Div('bin', css_class='col-md-4'),
                css_class='row'),
            Div(
                Div('desc', css_class='col-md-12'),
                css_class='row'),
        )


class RecentHistoryForm(forms.Form):
    start_date = forms.DateField(label="異動日期(起)")
    due_date = forms.DateField(label="異動日期(迄)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('start_date', css_class='col-md-3'),
                Div('due_date', css_class='col-md-3'),
                Div(Submit('search', '查詢', css_class='btn btn-info'),
                    css_class='col-md-3 d-flex align-items-center search_btn_fix pt-3'),
                css_class='row'),
        )

        self.fields['start_date'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
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


class ItemHistoryForm(forms.Form):
    start_date = forms.DateField(label="異動日期(起)")
    due_date = forms.DateField(label="異動日期(迄)")
    keyword = forms.CharField(max_length=50, label="料號|關鍵字", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('start_date', css_class='col-md-3'),
                Div('due_date', css_class='col-md-3'),
                Div('keyword', css_class='col-md-3'),
                Div(Submit('search', '查詢', css_class='btn btn-info'),
                    css_class='col-md-3 d-flex align-items-center search_btn_fix pt-3'),
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


class TransferSearchForm(forms.Form):
    keyword = forms.CharField(max_length=50, label="料號|關鍵字", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('keyword', css_class='col-md-4'),
                Div(Submit('search', '查詢', css_class='btn btn-info'),
                    css_class='col-md-2 d-flex align-items-center search_btn_fix pt-3'),
                css_class='row'),
        )


class TransferForm(forms.Form):
    storage = forms.ModelChoiceField(required=True, label="Storage", queryset=Storage.objects.all())
    location = forms.ModelChoiceField(required=True, label="Location", queryset=Location.objects.none())
    bin = forms.ModelChoiceField(required=True, label="Bin儲格", queryset=Bin.objects.none())
    qty = forms.CharField(max_length=50, label="數量", required=True)
    desc = forms.CharField(max_length=50, label="備註", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('bin', css_class='col-md-9'),
                Div('qty', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('desc', css_class='col-md-12'),
                css_class='row'),
        )


class ItemBinForm(forms.Form):
    item_code = forms.CharField(max_length=50, label="料號", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('item_code', css_class='col-md-4'),
                Div(Submit('search', '查詢', css_class='btn btn-info'),
                    css_class='col-md-2 d-flex align-items-center search_btn_fix pt-3'),
                css_class='row'),
        )


class NewItemBinForm(forms.Form):
    storage = forms.ModelChoiceField(required=True, label="Storage", queryset=Storage.objects.all())
    location = forms.ModelChoiceField(required=False, label="Location", queryset=Location.objects.none())
    bin = forms.ModelChoiceField(required=False, label="儲格", queryset=Bin.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('storage', css_class='col-md-3'),
                Div('location', css_class='col-md-3'),
                Div('bin', css_class='col-md-3'),
                Div(Submit('add', '新增', css_class='btn btn-info'),
                    css_class='col-md-3 d-flex align-items-center search_btn_fix pt-3'),
                css_class='row'),
        )


class StorageEditForm(forms.ModelForm):
    storage_code = forms.CharField(max_length=50, label="倉別", required=True)
    desc = forms.CharField(max_length=50, label="說明", required=True)
    enable = forms.BooleanField(required=False)

    class Meta:
        model = Storage
        fields = ('storage_code', 'desc', 'enable')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['storage_code'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('storage_code', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('desc', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('enable', css_class='col-md-3'),
                css_class='row'),
        )


class LocationEditForm(forms.ModelForm):
    storage = forms.ModelChoiceField(required=True, label="Storage", queryset=Storage.objects.all())
    location_code = forms.CharField(max_length=10, label="Location Code", required=True)
    location_name = forms.CharField(max_length=20, label="Location Name", required=True)
    desc = forms.CharField(max_length=50, label="說明", required=True)
    enable = forms.BooleanField(initial={'enable': True}, required=False)

    class Meta:
        model = Location
        fields = ('storage', 'location_code', 'location_name', 'desc', 'enable')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('storage', css_class='col-md-4'),
                Div('location_code', css_class='col-md-4'),
                css_class='row'),
            Div(
                Div('location_name', css_class='col-md-4'),
                Div('desc', css_class='col-md-4'),
                css_class='row'),
            Div(
                Div('enable', css_class='col-md-4'),
                css_class='row'),
        )


class BinEditForm(forms.ModelForm):
    location = forms.ModelChoiceField(required=True, label="Location", queryset=Location.objects.all())
    bin_code = forms.CharField(max_length=20, label="Bin Code", required=True)
    bin_name = forms.CharField(max_length=20, label="Bin Name", required=True)
    enable = forms.BooleanField(initial={'enable': True}, required=False)

    class Meta:
        model = Bin
        fields = ('location', 'bin_code', 'bin_name', 'enable')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('location', css_class='col-md-4'),
                css_class='row'),
            Div(
                Div('bin_code', css_class='col-md-4'),
                Div('bin_name', css_class='col-md-4'),
                css_class='row'),
            Div(
                Div('enable', css_class='col-md-4'),
                css_class='row'),
        )


class StockInForm(forms.Form):
    apply_date = forms.DateField(label="異動日期")
    desc = forms.CharField(max_length=250, label="說明", required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))
    item_code = forms.CharField(max_length=11, label="料號", required=False,)
    qty = forms.CharField(max_length=10, label="數量", required=False, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('apply_date', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('desc', css_class='col-md-12'),
                css_class='row'),
            Div(
                Div('item_code', css_class='col-md-2'),
                Div(Button('search', '查詢', css_class='btn btn-info', onclick="popup();"),
                css_class='col-md-2 d-flex align-items-center pt-3'),
                Div('qty', css_class='col-md-2'),
                Div(HTML('<a href="#" class="btn btn-info"><i class="fas fa-plus-circle"></i> 加入</a>'),
                    css_class='col-md-2 d-flex align-items-center pt-3'),
                css_class='row'),
        )

        self.fields['apply_date'].widget = DatePickerInput(
            attrs={'value': (datetime.now()).strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )
