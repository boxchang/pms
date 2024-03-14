from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from stock.forms import StorageEditForm
from stock.models import Storage

# Storage 編輯
@login_required
def location_setting(request):
    storages = Storage.objects.all()
    return render(request, 'stock/storage.html', locals())

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

