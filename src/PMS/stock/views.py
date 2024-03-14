from django.shortcuts import render

def search(request):
    return render(request, 'stock/search.html', locals())
