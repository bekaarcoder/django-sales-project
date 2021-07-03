from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from .utils import get_customer_from_id, get_salesman_from_id, get_chart


@login_required
def home_view(request):
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    no_data = None
    form = SalesSearchForm(request.POST or None)
    report_form = ReportForm

    if request.method == "POST":
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        chart_type = request.POST.get("chart_type")
        results_by = request.POST.get("results_by")

        # select * from sales where created <= date_to and created >= date_from
        qs = Sale.objects.filter(
            created__date__lte=date_to, created__date__gte=date_from
        )

        # If query set exists for the given dates
        if len(qs) > 0:
            # Create a sales dataframe from the queryset list
            sales_df = pd.DataFrame(qs.values())

            # Update the customer_id and salesman_id column in the dataframe
            sales_df["customer_id"] = sales_df["customer_id"].apply(
                get_customer_from_id
            )
            sales_df["saleman_id"] = sales_df["saleman_id"].apply(
                get_salesman_from_id
            )
            sales_df["created"] = sales_df["created"].apply(
                lambda x: x.strftime("%Y-%m-%d")
            )
            sales_df["updated"] = sales_df["updated"].apply(
                lambda x: x.strftime("%Y-%m-%d")
            )

            # Rename the column name
            sales_df = sales_df.rename(
                {
                    "customer_id": "customer",
                    "saleman_id": "salesman",
                    "id": "sales_id",
                },
                axis=1,
            )

            positions_data = []
            for sale in qs:
                for pos in sale.get_positions():
                    obj = {
                        "position_id": pos.id,
                        "product": pos.product.name,
                        "quantity": pos.quantity,
                        "price": pos.price,
                        "sales_id": pos.get_sales_id(),
                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on="sales_id")

            df = merged_df.groupby("transaction_id", as_index=False)[
                "price"
            ].agg("sum")

            # chart = get_chart(
            #     chart_type, df, labels=df["transaction_id"].values
            # )

            chart = get_chart(chart_type, sales_df, results_by)

            # Convert dataframe to html
            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()

        else:
            no_data = "No data available for the selected range."

    context = {
        "form": form,
        "report_form": report_form,
        "sales_df": sales_df,
        "positions_df": positions_df,
        "merged_df": merged_df,
        "df": df,
        "chart": chart,
        "no_data": no_data,
    }
    return render(request, "sales/home.html", context)


class SalesListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = "sales/main.html"


class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = "sales/detail.html"
