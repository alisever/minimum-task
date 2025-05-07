import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def upload_url():
    return reverse("upload_emissions")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "file_path, expected_count",
    [
        ("air_travel.csv", 9),
        ("electricity.csv", 19),
        ("purchased_goods_and_services.csv", 29),
    ],
)
def test_fixture_upload(client, upload_url, file_path, expected_count):
    with open(os.path.join(FIXTURES_DIR, file_path), "rb") as f:
        file_bytes = f.read()

    file = SimpleUploadedFile("file.csv", file_bytes, content_type="text/csv")
    response = client.post(upload_url, {"file": file}, format="multipart")
    print(response.data)
    assert response.status_code == 201
    assert response.data["created"] == expected_count
