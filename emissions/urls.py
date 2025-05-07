from django.urls import path

from emissions import views

urlpatterns = [
    path("upload-emissions/", views.EmissionUpload.as_view(), name="upload_emissions"),
    path("emissions/", views.EmissionPage.as_view(), name="emission_page"),
    path("emissions/table/", views.EmissionTablePartial.as_view(), name="emission_table"),
]
