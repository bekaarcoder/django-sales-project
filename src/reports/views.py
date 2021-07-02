from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.utils.dateparse import parse_date
from profiles.models import Profile
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView, DetailView, TemplateView
from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer
import csv


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


class UploadTemplateView(TemplateView):
    template_name = "reports/from_file.html"


def csv_upload_view(request):
    print("file is being uploaded")
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        obj = CSV.objects.create(file_name=csv_file)

        # open csv file
        with open(obj.file_name.path, "r") as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                transaction_id = row[1]
                product = row[2]
                quantity = int(row[3])
                customer = row[4]
                created = parse_date(row[5])

                try:
                    product_obj = Product.objects.get(
                        name__iexact=product
                    )  # iexact is to ignore the case-sensitive
                except Product.DoesNotExist:
                    product_obj = None

                if product_obj is not None:
                    customer_obj, _ = Customer.objects.get_or_create(
                        name=customer
                    )
                    salesman_obj = Profile.objects.get(user=request.user)
                    position_obj = Position.objects.create(
                        product=product_obj, quantity=quantity, created=created
                    )
                    sale_obj, _ = Sale.objects.get_or_create(
                        transaction_id=transaction_id,
                        customer=customer_obj,
                        saleman=salesman_obj,
                        created=created,
                    )
                    sale_obj.positions.add(position_obj)
                    sale_obj.save()
    return HttpResponse()


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
