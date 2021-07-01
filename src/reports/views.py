from django.shortcuts import render, get_object_or_404
from django.conf import settings
from profiles.models import Profile
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
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


def render_pdf_view(request, pk):
    template_path = "reports/pdf.html"

    obj = get_object_or_404(Report, id=pk)
    context = {"object": obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    # To directly download the file
    # response["Content-Disposition"] = 'attachment; filename="report.pdf"'
    # To display the pdf in the browser
    response["Content-Disposition"] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response
