from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Customer


# =========================================
# CUSTOMER LIST
# =========================================

def customer_list(request):

    if not request.user.is_authenticated:
        return redirect("login")

    customers = Customer.objects.all().order_by("-created_at")

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()

    if search:

        customers = customers.filter(
            name__icontains=search
        ) | customers.filter(
            email__icontains=search
        ) | customers.filter(
            phone__icontains=search
        ) | customers.filter(
            company__icontains=search
        )

    if status:

        customers = customers.filter(
            status=status
        )

    context = {
        "customers": customers,
        "search": search,
        "selected_status": status,
    }

    return render(
        request,
        "customers.html",
        context
    )


# =========================================
# ADD CUSTOMER
# =========================================

def add_customer(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        company = request.POST.get("company", "").strip()
        address = request.POST.get("address", "").strip()
        status = request.POST.get("status", "Active")


        # REQUIRED FIELD VALIDATION

        if not name or not email or not phone:

            messages.error(
                request,
                "Name, email and phone are required."
            )

            return render(
                request,
                "customer_form.html"
            )


        # EMAIL DUPLICATE CHECK

        if Customer.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "A customer with this email already exists."
            )

            return render(
                request,
                "customer_form.html"
            )


        # CREATE CUSTOMER

        Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            company=company,
            address=address,
            status=status
        )


        messages.success(
            request,
            "Customer added successfully!"
        )

        return redirect("customers")


    return render(
        request,
        "customer_form.html"
    )


# =========================================
# EDIT CUSTOMER
# =========================================

def edit_customer(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    customer = get_object_or_404(
        Customer,
        id=id
    )


    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        company = request.POST.get("company", "").strip()
        address = request.POST.get("address", "").strip()
        status = request.POST.get("status", "Active")


        # REQUIRED FIELD VALIDATION

        if not name or not email or not phone:

            messages.error(
                request,
                "Name, email and phone are required."
            )

            return render(
                request,
                "customer_form.html",
                {
                    "customer": customer
                }
            )


        # EMAIL DUPLICATE CHECK

        if Customer.objects.filter(
            email=email
        ).exclude(
            id=customer.id
        ).exists():

            messages.error(
                request,
                "Another customer already uses this email."
            )

            return render(
                request,
                "customer_form.html",
                {
                    "customer": customer
                }
            )


        # UPDATE CUSTOMER

        customer.name = name
        customer.email = email
        customer.phone = phone
        customer.company = company
        customer.address = address
        customer.status = status

        customer.save()


        messages.success(
            request,
            "Customer updated successfully!"
        )

        return redirect("customers")


    return render(
        request,
        "customer_form.html",
        {
            "customer": customer
        }
    )


# =========================================
# DELETE CUSTOMER
# =========================================

def delete_customer(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    customer = get_object_or_404(
        Customer,
        id=id
    )


    if request.method == "POST":

        customer.delete()

        messages.success(
            request,
            "Customer deleted successfully!"
        )


    return redirect("customers")