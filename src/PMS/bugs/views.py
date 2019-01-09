from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect

from bases.models import Status, FormType
from bases.utils import save_data_index, get_serial_num, get_form_type, get_home_url
from bugs.forms import BugForm
from bugs.models import Bug, Bug_attachment


@login_required
def bug_create(request):
    if 'project_pk' in request.session:
        s_project = request.session['project_pk']
    if 'request_pk' in request.session:
        s_request = request.session['request_pk']

    init_status = Status.objects.get(status_en='Wait')

    if request.method == 'POST':
        form = BugForm(s_project, request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_type = get_form_type('BUG')
                    tmp_form = form.save(commit=False)
                    tmp_form.bug_no = get_serial_num(s_project, form_type)  # Bug單編碼
                    tmp_form.create_by = request.user
                    tmp_form.update_by = request.user
                    tmp_form.save()
                    save_data_index(s_project, form_type)  # Save serial number after success

                    if request.FILES.get('files1'):
                        bug_file = Bug_attachment(files=request.FILES['files1'])
                        bug_file.description = request.POST['description1']
                        bug_file.bug = tmp_form
                        bug_file.save()
                    if request.FILES.get('files2'):
                        bug_file = Bug_attachment(files=request.FILES['files2'])
                        bug_file.description = request.POST['description2']
                        bug_file.bug = tmp_form
                        bug_file.save()
            except Exception as e:
                Exception('Unexpected error: {}'.format(e))

            return redirect(tmp_form.get_absolute_url())
    else:
        if 'project_pk' in request.session:
            form = BugForm(s_project, initial={'project': s_project, 'status': init_status})
        elif 'project_pk' in request.session and 'request_pk' in request.session:
            form = BugForm(s_project, initial={'project': s_project, 'request': s_request, 'status': init_status})
        else:
            form = BugForm(s_project)


    return render(request, 'bugs/bug_edit.html', {'form': form})



@login_required
def bug_edit(request, pk):
    if pk:
        bug = Bug.objects.get(pk=pk)

    if 'project_pk' in request.session:
        s_project = request.session['project_pk']
    elif pk:
        s_project = Bug.project.pk

    if request.method == 'POST':

        form = BugForm(s_project, request.POST, instance=bug)
        if form.is_valid():
            try:
                with transaction.atomic():
                    tmp_form = form.save(commit=False)
                    if request.FILES.get('files1'):
                        bug_file = Bug_attachment(files=request.FILES['files1'])
                        bug_file.description = request.POST['description1']
                        bug_file.bug = tmp_form
                        bug_file.save()
                    if request.FILES.get('files2'):
                        bug_file = Bug_attachment(files=request.FILES['files2'])
                        bug_file.description = request.POST['description2']
                        bug_file.bug = tmp_form
                        bug_file.save()
                    tmp_form.save()
            except Exception as e:
                Exception('Unexpected error: {}'.format(e))
            return redirect(bug.get_absolute_url())
    else:
        form = BugForm(s_project, instance=bug)
    return render(request, 'bugs/bug_edit.html', {'form': form, 'bug': bug})

@login_required
def bug_list(request):
    bugs = Bug.objects.all()

    return render(request, 'bugs/bug_list.html', locals())


@login_required
def bug_detail(request, pk):
    try:
        bug = Bug.objects.get(pk=pk)
        bug_no = bug.bug_no

        files = Bug_attachment.objects.filter(bug=bug).all()
        form_type = FormType.objects.filter(type='BUG').first()

    except Bug.DoesNotExist:
        raise Http404

    return render(request, 'bugs/bug_detail.html', locals())


@login_required
def bug_delete(request, pk):
    bug = Bug.objects.get(pk=pk)
    bug.delete()
    return redirect(get_home_url(request))


@login_required
def bug_file_delete(request, pk):
    b = request.GET.get('b')
    if b:
        bug = Bug.objects.get(pk=b)
    obj = Bug_attachment.objects.get(pk=pk)
    if obj:
        obj.delete()
    return redirect(bug.get_absolute_url())