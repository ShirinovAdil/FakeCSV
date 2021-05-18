from django import forms
from schemas.models import SchemaModel, ColumnModel


class SchemaModelForm(forms.ModelForm):
    class Meta:
        model = SchemaModel
        fields = ('name', 'separator',)


ColumnFormset = forms.modelformset_factory(
    ColumnModel,
    fields='__all__',
    extra=4,
    exclude=['schema'],
)


class RowsForm(forms.Form):
    rows = forms.IntegerField()
