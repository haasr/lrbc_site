from django import forms

# Iterable tuple:
EXPORT_FORMATS = (
    ('CSV', 'CSV'),
    ('JSON', 'JSON (MongoDB)'),
    ('SQL', 'SQL inserts')
)

class ExportRecordsForm(forms.Form):
    table_name = forms.CharField(
        label='Table name',
        required=True
    )

    file_name = forms.CharField(
        label='File name',
        required=True
    )

    export_type = forms.ChoiceField(choices=EXPORT_FORMATS)
    time_period = forms.IntegerField(widget=forms.HiddenInput())
    end_date = forms.CharField(widget=forms.HiddenInput())