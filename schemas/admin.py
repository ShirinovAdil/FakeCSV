from django.contrib import admin
from schemas.models import ColumnModel, SchemaModel


class ColumnInLine(admin.StackedInline):
    model = ColumnModel


@admin.register(ColumnModel)
class ColumnInSchemaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "type", "schema"]


@admin.register(SchemaModel)
class SchemaAdmin(admin.ModelAdmin):
    inlines = [ColumnInLine]
    list_display = ["__str__", "status", "created_at"]
