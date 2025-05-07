import csv
import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from emissions.models import Emission


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def upload_url():
    return reverse("upload_emissions")


@pytest.fixture
def valid_air_travel_csv():
    file = io.StringIO()
    writer = csv.writer(file)
    writer.writerow(["Date", "Activity", "Distance travelled", "Distance units", "Flight range", "Passenger class"])
    writer.writerow(["01/01/2023", "Air Travel", "1000", "kilometres", "Short-haul", "Economy class"])
    file.seek(0)
    content = file.getvalue().encode("utf-8")
    file_object = SimpleUploadedFile("import.csv", content, content_type="text/csv")
    return file_object


@pytest.mark.django_db
def test_successful_upload(client, upload_url, valid_air_travel_csv):
    response = client.post(upload_url, {"file": valid_air_travel_csv}, format="multipart")
    print(response.data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["created"] == 1
    assert Emission.objects.count() == 1


def test_missing_file_upload(client, upload_url):
    response = client.post(upload_url, {}, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "file" in response.data


def test_invalid_file_type(client, upload_url):
    invalid_file = io.StringIO("Invalid content")
    invalid_file.seek(0)
    content = invalid_file.getvalue().encode("utf-8")
    invalid_file_object = SimpleUploadedFile("invalid_file.txt", content, content_type="text/plain")
    response = client.post(upload_url, {"file": invalid_file_object}, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "File must be a CSV." in response.data["file"][0]


def test_invalid_csv_headers(client, upload_url):
    invalid_file = io.StringIO("Foo,Bar\n1,2")
    invalid_file.seek(0)
    content = invalid_file.getvalue().encode("utf-8")
    invalid_file_object = SimpleUploadedFile("invalid_file.csv", content, content_type="text/csv")
    response = client.post(upload_url, {"file": invalid_file_object}, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Unknown header row" in response.data["file"][0]


def test_invalid_activity(client, upload_url, valid_air_travel_csv):
    file = io.StringIO()
    writer = csv.writer(file)
    writer.writerow(["Date", "Activity", "Distance travelled", "Distance units", "Flight range", "Passenger class"])
    writer.writerow(["01/01/2023", "Electricity", "1000", "kilometres", "Short-haul", "Economy"])
    file.seek(0)
    content = file.getvalue().encode("utf-8")
    file_object = SimpleUploadedFile("import.csv", content, content_type="text/csv")
    response = client.post(upload_url, {"file": file_object}, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        "Expected activity to be 'Air Travel' for air travel records."
        in response.data["non_field_errors"][0]["activity"]
    )
