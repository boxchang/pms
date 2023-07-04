from django.shortcuts import render


# 回主頁
from inventory.forms import OfficeInvForm, ItemFormset


def main(request):
    form = OfficeInvForm()
    item_formset = ItemFormset()
    return render(request, 'inventory/main.html', locals())


def apply(request):
    #form = OfficeInvForm()
    formset = ItemFormset(request.POST)
    return render(request, 'inventory/main.html', locals())
