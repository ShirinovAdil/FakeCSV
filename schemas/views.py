from django.shortcuts import render, redirect
from schemas.models import SchemaModel
from django.contrib.auth.models import User
from schemas.forms import *


def list_all_schemas(request):
    """
    Lists all schemas of a logged in user
    """
    current_user = User.objects.get(pk=request.user.pk)
    all_schemas = SchemaModel.objects.filter(user=current_user)
    return render(request, 'schemas/list_all_schemas.html', {'schemas': all_schemas})


def create_schema(request):
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

