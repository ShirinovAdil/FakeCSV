from django import forms
from schemas.models import SchemaModel, ColumnModel


class SchemaModelForm(forms.ModelForm):
    class Meta:
        model = SchemaModel
        fields = ('name', 'separator',)


ColumnFormset = forms.modelformset_factory(
    ColumnModel,
    fields='__all__',
    extra=1,
    exclude=['schema'],
)
