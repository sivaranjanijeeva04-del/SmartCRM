# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from customers.models import Customer
from leads.models import Lead
from sales.models import Deal
from tasks.models import Task


# =========================================
# SIGNUP
# =========================================

def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("signup")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully!"
        )

        return redirect("login")

    return render(request, "signup.html")


# =========================================
# LOGIN
# =========================================

def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Remember Me
            if remember:
                # Keep user logged in for 30 days
                request.session.set_expiry(60 * 60 * 24 * 30)
            else:
                # Session expires when browser is closed
                request.session.set_expiry(0)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password!"
        )

        return redirect("login")

    return render(request, "login.html")
# =========================================
# LOGOUT
# =========================================

def logout_view(request):

    logout(request)

    return redirect("login")


# =========================================
# DASHBOARD
# =========================================

def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")


    # =====================================
    # CUSTOMERS
    # =====================================

    total_customers = Customer.objects.count()

    active_customers = Customer.objects.filter(
        status="Active"
    ).count()


    # =====================================
    # LEADS
    # =====================================

    total_leads = Lead.objects.count()

    active_leads = Lead.objects.filter(
        status__in=[
            "New",
            "Contacted",
            "Qualified"
        ]
    ).count()

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
    # SALES
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


    total_revenue = Deal.objects.filter(
        status="Won"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    # =====================================
    # MONTHLY SALES
    # =====================================

    monthly_sales = (
        Deal.objects
        .filter(status="Won")
        .annotate(
            month=TruncMonth("created_at")
        )
        .values("month")
        .annotate(
            revenue=Sum("amount")
        )
        .order_by("month")
    )


    sales_data = []


    for sale in monthly_sales:

        sales_data.append({
            "month": sale["month"].strftime("%b"),
            "revenue": float(sale["revenue"] or 0)
        })


    # =====================================
    # TASKS
    # =====================================

    pending_tasks = Task.objects.filter(
        status__in=[
            "Pending",
            "In Progress"
        ]
    ).count()


    # =====================================
    # RECENT CUSTOMERS
    # =====================================

    recent_customers = Customer.objects.all().order_by(
        "-created_at"
    )[:5]


    # =====================================
    # UPCOMING TASKS
    # =====================================

    upcoming_tasks = Task.objects.filter(
        status__in=[
            "Pending",
            "In Progress"
        ]
    ).order_by(
        "due_date",
        "due_time"
    )[:5]


    # =====================================
    # CONTEXT
    # =====================================

    context = {

        "total_customers": total_customers,
        "active_customers": active_customers,

        "total_leads": total_leads,
        "active_leads": active_leads,
        "converted_leads": converted_leads,

        "new_leads": new_leads,
        "contacted_leads": contacted_leads,
        "qualified_leads": qualified_leads,
        "lost_leads": lost_leads,

        "total_deals": total_deals,
        "open_deals": open_deals,
        "won_deals": won_deals,
        "lost_deals": lost_deals,

        "total_revenue": total_revenue,

        "pending_tasks": pending_tasks,

        "recent_customers": recent_customers,
        "upcoming_tasks": upcoming_tasks,

        "sales_data": sales_data,
    }


    return render(
        request,
        "dashboard.html",
        context
    )


# =========================================
# PROFILE / SETTINGS
# =========================================

def profile(request):

    if not request.user.is_authenticated:
        return redirect("login")


    user = request.user


    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")


        # USERNAME

        if username and username != user.username:

            if User.objects.filter(
                username=username
            ).exclude(
                id=user.id
            ).exists():

                messages.error(
                    request,
                    "Username already exists!"
                )

                return redirect("profile")


            user.username = username


        # EMAIL

        if email:

            if User.objects.filter(
                email=email
            ).exclude(
                id=user.id
            ).exists():

                messages.error(
                    request,
                    "Email already registered!"
                )

                return redirect("profile")


            user.email = email


        user.save()


        messages.success(
            request,
            "Profile updated successfully!"
        )


        return redirect("profile")


    return render(
        request,
        "profile.html",
        {
            "user": user
        }
    )