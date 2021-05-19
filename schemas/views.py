from django.shortcuts import render, redirect, HttpResponse, Http404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django import forms
from django.contrib.auth.decorators import login_required


from celery.result import AsyncResult

from schemas.forms import *
from schemas.services.generate_data import *
from schemas.tasks import make_csv_file
from schemas.models import *
from django.forms.models import model_to_dict

import os
import mimetypes


@login_required
def home(request):
    return redirect('schemas:list_all_schemas')


@login_required
def list_all_schemas(request):
    """
    Lists all schemas of a logged in user
    """
    current_user = User.objects.get(pk=request.user.pk)
    all_schemas = SchemaModel.objects.filter(user=current_user)
    return render(request, 'schemas/list_all_schemas.html', {'schemas': all_schemas})


@login_required
def create_schema(request):
    """
    Create a schema with a columns specified.
    Using formsets to dynamically add and remove forms
    """
    schema_form = SchemaModelForm(request.GET or None)
    formset = ColumnFormset(queryset=ColumnModel.objects.none())
    if request.method == 'POST':
        schema_form = SchemaModelForm(request.POST)
        formset = ColumnFormset(request.POST)
        if schema_form.is_valid() and formset.is_valid():
            schema = schema_form.save(commit=False)
            schema.user = User.objects.get(pk=request.user.pk)
            schema = schema_form.save()

            for form in formset:
                column = form.save(commit=False)
                column.schema = schema
                column.save()
                print(column.schema)
            return redirect('schemas:list_all_schemas')
    return render(request, "schemas/create_schema.html", {'form': schema_form, 'formset': formset})


@login_required
def edit_schema(request, pk):
    """
    Edit the schema structure
    """
    schema_to_edit = SchemaModel.objects.get(id=pk)
    columns = ColumnModel.objects.filter(schema_id=pk)
    schema_form = SchemaModelForm(initial=model_to_dict(schema_to_edit))
    Formset = forms.modelformset_factory(ColumnModel, extra=0, fields=['id', 'name', 'type', 'quantity_range_lower', 'quantity_range_upper', 'order'])
    formset = Formset(initial=[{'id': x.id} for x in schema_to_edit.column_in_schemas.all()], queryset=ColumnModel.objects.filter(schema_id=pk))
    if request.method == 'POST':
        schema_form = SchemaModelForm(request.POST, instance=schema_to_edit)
        formset = ColumnFormset(request.POST, initial=[x for x in schema_to_edit.column_in_schemas.all()])
        if schema_form.is_valid() and formset.is_valid():
            schema = schema_form.save()
            formset.save()
            return redirect('schemas:list_all_schemas')
        else:
            print(formset.errors)
    return render(request, "schemas/edit_schema.html", {'form': schema_form, 'formset': formset})


@login_required
@csrf_exempt
def task_state(request):
    """
    Endpoint returning Task's state
    """
    response_data = 'Fail'
    task_id = request.POST['task_id'] or None
    print(f"task_id {task_id}")
    if task_id is not None:
        result = AsyncResult(task_id)  # should be task.AsyncResult???
        print(result.get())
        response_data = {
            'state': result.state,
            'details': result.info,
        }
    else:
        response_data = 'No task_id in the request'
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required
def view_schema(request, pk):
    """
    Render datasets and handle post request via AJAX
    """
    schema = SchemaModel.objects.get(pk=pk)
    form = RowsForm(request.POST or None)
    context = {
        'schema': schema,
        'form': form,
    }
    if request.method == 'POST':
        rows = int(request.POST.get('rows'))
        job = make_csv_file.apply_async((schema.id, rows))
        try:
            del request.session['task_id']
        except KeyError:
            pass
        request.session['task_id'] = job.id
        return redirect('schemas:view_schema', pk=pk)
    return render(request, 'schemas/view_schema.html', context)


@login_required
def delete_schema(request, schema_id):
    # Delete selected problem from list
    SchemaModel.objects.filter(pk=schema_id).delete()
    return redirect('schemas:list_all_schemas')


@login_required
def delete_file(request, file_id):
    # Delete selected file from db
    schema_id = SchemaFile.objects.get(pk=file_id).schema.id

    SchemaFile.objects.filter(pk=file_id).delete()
    return redirect('schemas:view_schema', pk=schema_id)


# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404


# def download_file(request, path):
#     print("here")
#     # fill these variables with real values
#     fl_path = os.path.join(settings.MEDIA_ROOT)
#     filename = path.rsplit('/', 1)[-1]
#     print(filename)
#     fl = open(fl_path, 'r')
#     mime_type, _ = mimetypes.guess_type(fl_path)
#     response = HttpResponse(fl, content_type=mime_type)
#     response['Content-Disposition'] = "attachment; filename=%s" % filename
#     return response