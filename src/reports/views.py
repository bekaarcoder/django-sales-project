from django.shortcuts import render
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView, DetailView


def create_report_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        remarks = request.POST.get("remarks")
        image = request.POST.get("image")
        author = Profile.objects.get(user=request.user)

        img = get_report_image(image)

        Report.objects.create(
            name=name, remarks=remarks, image=img, author=author
        )

        return JsonResponse({"message": "Report saved Successfully."})


# def report_view(request):
#     return render(request, "reports/home.html")


class ReportListView(ListView):
    model = Report
    template_name = "reports/home.html"


class ReportDetailView(DetailView):
    model = Report
    template_name = "reports/detail.html"
