from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum

from .models import Deal
from customers.models import Customer
from leads.models import Lead


# =========================================
# SALES / DEAL LIST
# =========================================

def deal_list(request):

    if not request.user.is_authenticated:
        return redirect("login")


    deals = Deal.objects.all().order_by("-created_at")


    # =====================================
    # SEARCH
    # =====================================

    search = request.GET.get(
        "search",
        ""
    ).strip()


    if search:

        deals = deals.filter(

            deal_name__icontains=search

        ) | deals.filter(

            customer__name__icontains=search

        ) | deals.filter(

            customer__company__icontains=search

        )


    # =====================================
    # FILTERS
    # =====================================

    status = request.GET.get(
        "status",
        ""
    ).strip()


    stage = request.GET.get(
        "stage",
        ""
    ).strip()


    if status:

        deals = deals.filter(
            status=status
        )


    if stage:

        deals = deals.filter(
            stage=stage
        )


    # =====================================
    # SALES SUMMARY
    # =====================================

    total_deals = Deal.objects.count()


    open_deals = Deal.objects.filter(
        status="Open"
    ).count()


    won_deals = Deal.objects.filter(
        status="Won"
    ).count()


    lost_deals = Deal.objects.filter(
        status="Lost"
    ).count()


    # =====================================
    # REVENUE
    # =====================================

    total_revenue = Deal.objects.filter(
        status="Won"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    # =====================================
    # OPEN PIPELINE VALUE
    # =====================================

    pipeline_value = Deal.objects.filter(
        status="Open"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    # =====================================
    # CONTEXT
    # =====================================

    context = {

        "deals": deals,

        "search": search,

        "selected_status": status,

        "selected_stage": stage,

        "total_deals": total_deals,

        "open_deals": open_deals,

        "won_deals": won_deals,

        "lost_deals": lost_deals,

        "total_revenue": total_revenue,

        "pipeline_value": pipeline_value,

    }


    return render(
        request,
        "sales.html",
        context
    )


# =========================================
# ADD DEAL
# =========================================

def add_deal(request):

    if not request.user.is_authenticated:
        return redirect("login")


    if request.method == "POST":

        deal_name = request.POST.get(
            "deal_name",
            ""
        ).strip()


        customer_id = request.POST.get(
            "customer"
        )


        lead_id = request.POST.get(
            "lead"
        )


        amount = request.POST.get(
            "amount"
        )


        stage = request.POST.get(
            "stage",
            "New"
        )


        status = request.POST.get(
            "status",
            "Open"
        )


        expected_close_date = request.POST.get(
            "expected_close_date"
        )


        notes = request.POST.get(
            "notes",
            ""
        ).strip()


        # =================================
        # VALIDATION
        # =================================

        if not deal_name or not customer_id or not amount:

            messages.error(
                request,
                "Deal name, customer and amount are required."
            )


            customers = Customer.objects.all()

            leads = Lead.objects.all()


            return render(
                request,
                "deal_form.html",
                {
                    "customers": customers,
                    "leads": leads,
                }
            )


        # =================================
        # CUSTOMER
        # =================================

        customer = get_object_or_404(
            Customer,
            id=customer_id
        )


        # =================================
        # LEAD
        # =================================

        lead = None


        if lead_id:

            lead = get_object_or_404(
                Lead,
                id=lead_id
            )


        # =================================
        # CREATE DEAL
        # =================================

        Deal.objects.create(

            deal_name=deal_name,

            customer=customer,

            lead=lead,

            amount=amount,

            stage=stage,

            status=status,

            expected_close_date=(
                expected_close_date
                if expected_close_date
                else None
            ),

            notes=notes

        )


        messages.success(
            request,
            "Deal added successfully!"
        )


        return redirect(
            "sales"
        )


    customers = Customer.objects.all()

    leads = Lead.objects.all()


    return render(
        request,
        "deal_form.html",
        {
            "customers": customers,
            "leads": leads,
        }
    )


# =========================================
# EDIT DEAL
# =========================================

def edit_deal(request, id):

    if not request.user.is_authenticated:
        return redirect("login")


    deal = get_object_or_404(
        Deal,
        id=id
    )


    if request.method == "POST":

        deal_name = request.POST.get(
            "deal_name",
            ""
        ).strip()


        customer_id = request.POST.get(
            "customer"
        )


        lead_id = request.POST.get(
            "lead"
        )


        amount = request.POST.get(
            "amount"
        )


        stage = request.POST.get(
            "stage",
            "New"
        )


        status = request.POST.get(
            "status",
            "Open"
        )


        expected_close_date = request.POST.get(
            "expected_close_date"
        )


        notes = request.POST.get(
            "notes",
            ""
        ).strip()


        # =================================
        # VALIDATION
        # =================================

        if not deal_name or not customer_id or not amount:

            messages.error(
                request,
                "Deal name, customer and amount are required."
            )


            customers = Customer.objects.all()

            leads = Lead.objects.all()


            return render(
                request,
                "deal_form.html",
                {
                    "deal": deal,
                    "customers": customers,
                    "leads": leads,
                }
            )


        # =================================
        # UPDATE
        # =================================

        deal.deal_name = deal_name


        deal.customer = get_object_or_404(
            Customer,
            id=customer_id
        )


        if lead_id:

            deal.lead = get_object_or_404(
                Lead,
                id=lead_id
            )

        else:

            deal.lead = None


        deal.amount = amount

        deal.stage = stage

        deal.status = status


        deal.expected_close_date = (

            expected_close_date
            if expected_close_date
            else None

        )


        deal.notes = notes


        deal.save()


        messages.success(
            request,
            "Deal updated successfully!"
        )


        return redirect(
            "sales"
        )


    customers = Customer.objects.all()

    leads = Lead.objects.all()


    return render(
        request,
        "deal_form.html",
        {
            "deal": deal,
            "customers": customers,
            "leads": leads,
        }
    )


# =========================================
# DELETE DEAL
# =========================================

def delete_deal(request, id):

    if not request.user.is_authenticated:
        return redirect("login")


    deal = get_object_or_404(
        Deal,
        id=id
    )


    if request.method == "POST":

        deal.delete()


        messages.success(
            request,
            "Deal deleted successfully!"
        )


    return redirect(
        "sales"
    )