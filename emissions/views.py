from django.db.models import Sum
from django.views.generic import ListView, TemplateView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from emissions.models import Emission
from emissions.serializers import EmissionUploadSerializer


class EmissionUpload(CreateAPIView):
    """
    Handles the process of uploading emission data by providing a view to create new emission entries.

    The serializer takes a single file, and chooses a sub-serializer to do the creation.
    """

    serializer_class = EmissionUploadSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_emissions = serializer.save()
        return Response({"created": len(created_emissions)}, status=status.HTTP_201_CREATED)


class EmissionPage(TemplateView):
    template_name = "emissions/emissions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activities"] = Emission.objects.values_list("activity", flat=True).distinct()
        return context


class EmissionTablePartial(ListView):
    model = Emission
    template_name = "emissions/partials/emission_table.html"
    context_object_name = "emissions"
    paginate_by = 20

    def get_queryset(self):
        qs = Emission.objects.all()

        if activity := self.request.GET.get("activity"):
            qs = qs.filter(activity=activity)
        if scope := self.request.GET.get("scope"):
            qs = qs.filter(scope=scope)
        if category := self.request.GET.get("category"):
            if category == "None":
                qs = qs.filter(category__isnull=True)
            else:
                qs = qs.filter(category=category)

        if ordering := self.request.GET.get("ordering"):
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by("-date")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["total_co2e"] = queryset.aggregate(total=Sum("co2e"))["total"] or 0
        context["co2e_by_activity"] = (
            queryset.values("activity").annotate(total_co2e=Sum("co2e")).order_by("-total_co2e")
        )
        context["scope"] = self.request.GET.get("scope", "")
        context["category"] = self.request.GET.get("category", "")
        context["scope_options"] = Emission.objects.values_list("scope", flat=True).distinct().order_by("scope")
        context["category_options"] = (
            Emission.objects.values_list("category", flat=True).distinct().order_by("category")
        )

        return context
