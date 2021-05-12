from django.urls import path, re_path, include
from schemas import views

app_name = "schemas"

urlpatterns = [
    path('schemas/', views.list_all_schemas, name='list_all_schemas'),
    path('schemas/create/', views.create_schema, name='create_schema'),
]
