from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Lead


# =========================================
# LEAD LIST
# =========================================

def lead_list(request):

    if not request.user.is_authenticated:
        return redirect("login")

    leads = Lead.objects.all().order_by("-created_at")

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    source = request.GET.get("source", "").strip()

    if search:
        leads = leads.filter(
            name__icontains=search
        ) | leads.filter(
            email__icontains=search
        ) | leads.filter(
            phone__icontains=search
        ) | leads.filter(
            company__icontains=search
        )

    if status:
        leads = leads.filter(status=status)

    if source:
        leads = leads.filter(source=source)

    context = {
        "leads": leads,
        "search": search,
        "selected_status": status,
        "selected_source": source,
    }

    return render(
        request,
        "leads.html",
        context
    )


# =========================================
# ADD LEAD
# =========================================

def add_lead(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        company = request.POST.get("company", "").strip()
        source = request.POST.get("source", "").strip()
        status = request.POST.get("status", "New").strip()
        notes = request.POST.get("notes", "").strip()

        # Required field validation

        if not name:
            messages.error(request, "Please enter the lead name.")
            return render(request, "lead_form.html")

        if not email:
            messages.error(request, "Please enter the email address.")
            return render(request, "lead_form.html")

        if not phone:
            messages.error(request, "Please enter the phone number.")
            return render(request, "lead_form.html")

        if not source:
            messages.error(request, "Please select a lead source.")
            return render(request, "lead_form.html")

        # Create Lead

        lead = Lead.objects.create(
            name=name,
            email=email,
            phone=phone,
            company=company,
            source=source,
            status=status,
            notes=notes
        )

        messages.success(
            request,
            f"Lead '{lead.name}' added successfully!"
        )

        return redirect("leads")

    return render(
        request,
        "lead_form.html"
    )


# =========================================
# EDIT LEAD
# =========================================

def edit_lead(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    lead = get_object_or_404(
        Lead,
        id=id
    )

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        company = request.POST.get("company", "").strip()
        source = request.POST.get("source", "").strip()
        status = request.POST.get("status", "New").strip()
        notes = request.POST.get("notes", "").strip()

        if not name:
            messages.error(request, "Please enter the lead name.")
            return render(
                request,
                "lead_form.html",
                {"lead": lead}
            )

        if not email:
            messages.error(request, "Please enter the email address.")
            return render(
                request,
                "lead_form.html",
                {"lead": lead}
            )

        if not phone:
            messages.error(request, "Please enter the phone number.")
            return render(
                request,
                "lead_form.html",
                {"lead": lead}
            )

        if not source:
            messages.error(request, "Please select a lead source.")
            return render(
                request,
                "lead_form.html",
                {"lead": lead}
            )

        lead.name = name
        lead.email = email
        lead.phone = phone
        lead.company = company
        lead.source = source
        lead.status = status
        lead.notes = notes

        lead.save()

        messages.success(
            request,
            f"Lead '{lead.name}' updated successfully!"
        )

        return redirect("leads")

    return render(
        request,
        "lead_form.html",
        {
            "lead": lead
        }
    )


# =========================================
# DELETE LEAD
# =========================================

def delete_lead(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    lead = get_object_or_404(
        Lead,
        id=id
    )

    if request.method == "POST":

        lead_name = lead.name

        lead.delete()

        messages.success(
            request,
            f"Lead '{lead_name}' deleted successfully!"
        )

    return redirect("leads")