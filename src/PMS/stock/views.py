from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from stock.forms import StorageEditForm, LocationEditForm, BinEditForm, StockInForm
from stock.models import Storage, Location, Bin


# Storage 編輯
@login_required
def storage_edit(request):
    form = StorageEditForm()
    if request.method == 'POST':
        pk = request.POST.get('pk')
        action = request.POST.get('action')
        storage = Storage.objects.get(pk=pk)
        if action == "edit":
            form = StorageEditForm(request.POST, instance=storage)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.update_by = request.user
                tmp_form.save()
                return redirect(reverse('location_setting'))

        else:
            form = StorageEditForm(instance=storage)

    return render(request, 'stock/storage_edit.html', locals())


def search(request):
    return render(request, 'stock/search.html', locals())

# Storage 編輯
@login_required
def location_setting(request):
    storages = Storage.objects.all()
    return render(request, 'stock/storage.html', locals())


# Location 編輯
@login_required
def location_list(request):
    if request.method == 'POST':
        storage_code = request.POST.get('pk')
        storage = Storage.objects.get(storage_code=storage_code)
        locations = Location.objects.filter(storage=storage).all()
    return render(request, 'stock/location.html', locals())


# Location 編輯
@login_required
def location_add(request):
    if request.method == 'POST':
        storage_code = request.POST.get('storage_code')
        storage = Storage.objects.get(storage_code=storage_code)
        form = LocationEditForm(initial={'storage': storage})
        form.fields['storage'].widget.attrs['disabled'] = True
        action = "add"
        return render(request, 'stock/location_edit.html', locals())


# Location 編輯
@login_required
def location_edit(request):
    if request.method == 'POST':
        storage_code = request.POST.get('storage_code')
        location_code = request.POST.get('location_code')
        if location_code:
            location = Location.objects.get(location_code=location_code)
        form = LocationEditForm(instance=location)
        form.fields['plant'].widget.attrs['disabled'] = True
        form.fields['storage'].widget.attrs['disabled'] = True
        form.fields['location_code'].widget.attrs['readonly'] = True
        action = "edit"
        return render(request, 'stock/location_edit.html', locals())


# Location 編輯
@login_required
def location_save(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "edit":
            location_code = request.POST.get('location_code')
            if location_code:
                location = Location.objects.get(location_code=location_code)

            form = LocationEditForm(request.POST, instance=location)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.update_by = request.user
                tmp_form.save()
        elif action == "add":
            form = LocationEditForm(request.POST)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.update_by = request.user
                tmp_form.save()

        storage_code = request.POST.get('storage_code')
        storage = Storage.objects.get(storage_code=storage_code)
        locations = Location.objects.filter(storage=storage).all()
        return render(request, 'stock/location.html', locals())
    return render(request, 'stock/location_edit.html', locals())

# 儲格編輯
@login_required
def bin_list(request, storage_code, location_code):
    bins = Bin.objects.filter(location=location_code).all()
    return render(request, 'stock/bin.html', locals())


# 儲格編輯
@login_required
def bin_add(request):
    if request.method == 'POST':
        storage_code = request.POST.get('storage_code')
        location_code = request.POST.get('location_code')
        location = Location.objects.get(location_code=location_code)
        form = BinEditForm(initial={'location': location})
        form.fields['location'].widget.attrs['disabled'] = True
        action = "add"
        return render(request, 'stock/bin_edit.html', locals())


# 儲格編輯
@login_required
def bin_edit(request):
    if request.method == 'POST':
        storage_code = request.POST.get('storage_code')
        location_code = request.POST.get('location_code')
        bin_code = request.POST.get('bin_code')
        if bin_code:
            bin = Bin.objects.get(bin_code=bin_code)
        form = BinEditForm(instance=bin)
        form.fields['location'].widget.attrs['disabled'] = True
        form.fields['bin_code'].widget.attrs['readonly'] = True
        action = "edit"
        return render(request, 'stock/bin_edit.html', locals())


# 儲格編輯
@login_required
def bin_save(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "edit":
            bin_code = request.POST.get('bin_code')
            if bin_code:
                bin = Bin.objects.get(bin_code=bin_code)

            form = BinEditForm(request.POST, instance=bin)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.update_by = request.user
                tmp_form.save()
        elif action == "add":
            form = BinEditForm(request.POST)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.update_by = request.user
                tmp_form.save()

        location_code = request.POST.get('location_code')
        location = Location.objects.get(location_code=location_code)
        storage_code = location.storage.storage_code
        bins = Bin.objects.filter(location=location).all()
        return render(request, 'stock/bin.html', locals())
    return render(request, 'stock/bin_edit.html', locals())


# 入庫作業
@login_required
def stock_in(request):
    form = StockInForm()
    return render(request, 'stock/stock_in.html', locals())


# 出庫作業
@login_required
def stock_out(request):
    return render(request, 'stock/stock_out.html', locals())
