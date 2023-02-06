from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from bases.models import Status
from bugs.models import Bug
from problems.models import Problem
from projects.models import Project, Project_setting
from requests.models import Request
from requests.utils import update_process_rate
from users.models import CustomUser


@login_required
def index(request):
    #return render(request, 'assets/index.html', locals())
    return redirect(reverse('assets_main'))


def change_status(request):
    request_no = request.POST.get('request_no')
    new_status = request.POST.get('new_status')
    o_new_status = Status.objects.get(pk=new_status)
    the_request = Request.objects.filter(request_no=request_no).first()
    the_request.status = o_new_status
    the_request.process_rate = update_process_rate(the_request.request_no, o_new_status)
    the_request.save()

    result = {'message': 'good'}

    return JsonResponse(result, safe=False)
