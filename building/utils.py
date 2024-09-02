from urllib.parse import unquote, urlparse
from django.http import HttpResponse
import csv
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("/rentmate/firebase_config.json")
firebase_admin.initialize_app(cred, {"storageBucket": "rentmate-c6d88.appspot.com"})


def get_or_404(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def convert_string_to_display(string):
    words = string.split(" ")
    capitalized_words = [word.capitalize() for word in words]
    display_string = " ".join(capitalized_words)
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


def delete_images_form_firebase(urls):
    image_file_names = []
    if not urls:
        return
    for url in urls:
        parsed_url = urlparse(url)
        # Extract the path component and decode it
        decoded_path = unquote(parsed_url.path)
        # Extract the filename from the path
        filename = decoded_path.split("appspot.com/o/")[-1].strip()
        image_file_names.append(filename)
    bucket = storage.bucket()
    for image in image_file_names:
        blob = bucket.blob(image)
        blob.delete()
