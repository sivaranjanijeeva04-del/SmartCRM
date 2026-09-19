from django.shortcuts import render, redirect
from django.db.models import Sum

from customers.models import Customer
from leads.models import Lead
from sales.models import Deal
from tasks.models import Task


# =========================================
# REPORTS DASHBOARD
# =========================================

def reports_dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")


    # =====================================
    # CUSTOMER REPORT
    # =====================================

    total_customers = Customer.objects.count()

    active_customers = Customer.objects.filter(
        status="Active"
    ).count()

    inactive_customers = Customer.objects.filter(
        status="Inactive"
    ).count()

    pending_customers = Customer.objects.filter(
        status="Pending"
    ).count()


    # =====================================
    # LEAD REPORT
    # =====================================

    total_leads = Lead.objects.count()

    new_leads = Lead.objects.filter(
        status="New"
    ).count()

    contacted_leads = Lead.objects.filter(
        status="Contacted"
    ).count()

    qualified_leads = Lead.objects.filter(
        status="Qualified"
    ).count()

    converted_leads = Lead.objects.filter(
        status="Converted"
    ).count()

    lost_leads = Lead.objects.filter(
        status="Lost"
    ).count()


    # =====================================
    # SALES REPORT
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


    pipeline_value = Deal.objects.filter(
        status="Open"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    # =====================================
    # DEAL STAGE REPORT
    # =====================================

    new_deals = Deal.objects.filter(
        stage="New"
    ).count()

    proposal_deals = Deal.objects.filter(
        stage="Proposal"
    ).count()

    negotiation_deals = Deal.objects.filter(
        stage="Negotiation"
    ).count()


    # =====================================
    # TASK REPORT
    # =====================================

    total_tasks = Task.objects.count()

    pending_tasks = Task.objects.filter(
        status="Pending"
    ).count()

    in_progress_tasks = Task.objects.filter(
        status="In Progress"
    ).count()

    completed_tasks = Task.objects.filter(
        status="Completed"
    ).count()

    cancelled_tasks = Task.objects.filter(
        status="Cancelled"
    ).count()


    # =====================================
    # TASK PRIORITY
    # =====================================

    high_priority_tasks = Task.objects.filter(
        priority="High"
    ).exclude(
        status__in=[
            "Completed",
            "Cancelled"
        ]
    ).count()

    medium_priority_tasks = Task.objects.filter(
        priority="Medium"
    ).exclude(
        status__in=[
            "Completed",
            "Cancelled"
        ]
    ).count()

    low_priority_tasks = Task.objects.filter(
        priority="Low"
    ).exclude(
        status__in=[
            "Completed",
            "Cancelled"
        ]
    ).count()


    # =====================================
    # CONTEXT
    # =====================================

    context = {

        # Customers
        "total_customers": total_customers,
        "active_customers": active_customers,
        "inactive_customers": inactive_customers,
        "pending_customers": pending_customers,

        # Leads
        "total_leads": total_leads,
        "new_leads": new_leads,
        "contacted_leads": contacted_leads,
        "qualified_leads": qualified_leads,
        "converted_leads": converted_leads,
        "lost_leads": lost_leads,

        # Sales
        "total_deals": total_deals,
        "open_deals": open_deals,
        "won_deals": won_deals,
        "lost_deals": lost_deals,

        # Revenue
        "total_revenue": total_revenue,
        "pipeline_value": pipeline_value,

        # Deal stages
        "new_deals": new_deals,
        "proposal_deals": proposal_deals,
        "negotiation_deals": negotiation_deals,

        # Tasks
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completed_tasks": completed_tasks,
        "cancelled_tasks": cancelled_tasks,

        # Priority
        "high_priority_tasks": high_priority_tasks,
        "medium_priority_tasks": medium_priority_tasks,
        "low_priority_tasks": low_priority_tasks,

    }


    return render(
        request,
        "reports.html",
        context
    )