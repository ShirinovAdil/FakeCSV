from django.urls import path
from schemas import views


app_name = "schemas"

urlpatterns = [
    path('', views.home, name='home'),
    path('schemas/', views.list_all_schemas, name='list_all_schemas'),
    path('schemas/create/', views.create_schema, name='create_schema'),
    path('schemas/view/<int:pk>', views.view_schema, name='view_schema'),
    path('schemas/edit/<int:pk>', views.edit_schema, name='edit_schema'),
    path('schemas/delete/<int:schema_id>', views.delete_schema, name='delete_schema'),
    path('schemas/delete/file/<int:file_id>', views.delete_file, name='delete_file'),

    path('schemas/view/task_state', views.task_state, name='task_state'),

    #path('media/<str:path>', views.download, name="download")
]