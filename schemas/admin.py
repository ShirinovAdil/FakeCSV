from django.contrib import admin
from schemas.models import ColumnModel, SchemaModel, SchemaFile


class ColumnInLine(admin.StackedInline):
    model = ColumnModel


class FileInLine(admin.StackedInline):
    model = SchemaFile


@admin.register(SchemaFile)
class FileInSchemaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "file", "status"]


@admin.register(ColumnModel)
class ColumnInSchemaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "type", "schema"]


@admin.register(SchemaModel)
class SchemaAdmin(admin.ModelAdmin):
    inlines = [ColumnInLine, FileInLine]
    list_display = ["__str__", "status", "created_at"]
