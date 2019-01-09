import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from bases.utils import *
from problems.forms import ProblemForm, ProblemReplyForm
from problems.models import *

@login_required
def problem_create(request):
    belong_to = ''

    p = request.GET.get('p')  #單號
    t = request.GET.get('t')  #單號類型

    if p:
        belong_to = p
    if t:
        belong_to_type = FormType.objects.filter(tid=t).first()

    if 'project_pk' in request.session:
        s_project = request.session['project_pk']
    if 'request_pk' in request.session:
        s_request = request.session['request_pk']

    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_type = get_form_type('PROBLEM')
                    tmp_form = form.save(commit=False)
                    tmp_form.problem_no = get_serial_num(s_project, form_type)  # 問題單編碼
                    tmp_form.create_by = request.user
                    tmp_form.update_by = request.user
                    tmp_form.belong_to_type = belong_to_type
                    tmp_form.belong_to = belong_to
                    tmp_form.save()
                    save_data_index(s_project, form_type)  # Save serial number after success

                    if request.FILES.get('files1'):
                        problem_file = Problem_attachment(files=request.FILES['files1'])
                        problem_file.description = request.POST['description1']
                        problem_file.problem = tmp_form
                        problem_file.save()
                    if request.FILES.get('files2'):
                        problem_file = Problem_attachment(files=request.FILES['files2'])
                        problem_file.description = request.POST['description2']
                        problem_file.problem = tmp_form
                        problem_file.save()

            except Exception as e:
                Exception('Unexpected error: {}'.format(e))

            return redirect(tmp_form.get_absolute_url())
    else:
        if 'project_pk' in request.session and 'request_pk' in request.session:
            form = ProblemForm(initial={'project': s_project, 'belong_to': s_request})
        else:
            form = ProblemForm()


    return render(request, 'problems/problem_edit.html', {'form': form})


@login_required
def problem_edit(request, pk):
    if pk:
        problem = Problem.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            try:
                with transaction.atomic():
                    tmp_form = form.save(commit=False)
                    if request.FILES.get('files1'):
                        problem_file = Problem_attachment(files=request.FILES['files1'])
                        problem_file.description = request.POST['description1']
                        problem_file.problem = tmp_form
                        problem_file.save()
                    if request.FILES.get('files2'):
                        problem_file = Problem_attachment(files=request.FILES['files2'])
                        problem_file.description = request.POST['description2']
                        problem_file.problem = tmp_form
                        problem_file.save()
                    tmp_form.save()
            except Exception as e:
                Exception('Unexpected error: {}'.format(e))

            return redirect(tmp_form.get_absolute_url())
    else:
        form = ProblemForm(instance=problem)
    return render(request, 'problems/problem_edit.html', {'form': form, 'problem': problem})


@login_required
def problem_list(request):
    problems = Problem.objects.all()

    return render(request, 'problems/problem_list.html', {'problems': problems})


@login_required
def problem_detail(request, pk):
    problem = Problem.objects.get(pk=pk)
    files = Problem_attachment.objects.filter(problem=problem).all()
    problem_reply_form = ProblemReplyForm()
    problem_replys = Problem_reply.objects.filter(problem_no=problem).all()
    table_cnt = range(3-files.count())
    return render(request, 'problems/problem_detail.html', locals())


@login_required
def problem_delete(request, pk):

    problem = Problem.objects.get(pk=pk)
    replys = Problem_reply.objects.filter(problem_no=problem)
    problem.delete()
    replys.delete()
    return redirect(get_home_url(request))


@login_required
def problem_file_delete(request, pk):
    p = request.GET.get('p')
    if p:
        problem = Problem.objects.get(pk=p)
    obj = Problem_attachment.objects.get(pk=pk)
    if obj:
        obj.delete()
    return redirect(problem.get_absolute_url())


@login_required
def problem_reply_create(request, pk):
    problem = Problem.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProblemReplyForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.problem_no = problem
            data.create_by = request.user
            data.update_by = request.user
            data.save()

    return redirect(problem.get_absolute_url())
