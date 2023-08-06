from django.http import HttpResponse
import csv


def get_or_404(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def convert_string_to_display(string):
    words = string.split('_')
    capitalized_words = [word.capitalize() for word in words]
    display_string = ' '.join(capitalized_words)
    return display_string


def data_export(data_list, column_names, datasetValues, filename, *args, **kwargs):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    writer = csv.DictWriter(response, column_names)
    writer.writeheader()
    for data in data_list:
        data = data.__dict__
        data_row = {}
        for column in column_names:
            data_row[column] = data[datasetValues[column]]
        writer.writerow(data_row)
    return response
