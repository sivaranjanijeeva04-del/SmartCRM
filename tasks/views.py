from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Task
from customers.models import Customer


# =========================================
# TASK LIST
# =========================================

def task_list(request):

    if not request.user.is_authenticated:
        return redirect("login")

    tasks = Task.objects.all().order_by(
        "due_date",
        "due_time"
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status = request.GET.get(
        "status",
        ""
    ).strip()

    priority = request.GET.get(
        "priority",
        ""
    ).strip()

    task_type = request.GET.get(
        "task_type",
        ""
    ).strip()


    # =====================================
    # SEARCH
    # =====================================

    if search:

        tasks = tasks.filter(

            title__icontains=search

        ) | tasks.filter(

            customer__name__icontains=search

        )


    # =====================================
    # STATUS FILTER
    # =====================================

    if status:

        tasks = tasks.filter(
            status=status
        )


    # =====================================
    # PRIORITY FILTER
    # =====================================

    if priority:

        tasks = tasks.filter(
            priority=priority
        )


    # =====================================
    # TASK TYPE FILTER
    # =====================================

    if task_type:

        tasks = tasks.filter(
            task_type=task_type
        )


    # =====================================
    # TASK SUMMARY
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


    high_priority_tasks = Task.objects.filter(
        priority="High"
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

        "tasks": tasks,

        "search": search,

        "selected_status": status,

        "selected_priority": priority,

        "selected_task_type": task_type,

        "total_tasks": total_tasks,

        "pending_tasks": pending_tasks,

        "in_progress_tasks": in_progress_tasks,

        "completed_tasks": completed_tasks,

        "high_priority_tasks": high_priority_tasks,

    }


    return render(
        request,
        "tasks.html",
        context
    )


# =========================================
# ADD TASK
# =========================================

def add_task(request):

    if not request.user.is_authenticated:
        return redirect("login")


    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        customer_id = request.POST.get(
            "customer"
        )

        task_type = request.POST.get(
            "task_type",
            "Follow-up"
        )

        due_date = request.POST.get(
            "due_date"
        )

        due_time = request.POST.get(
            "due_time"
        )

        priority = request.POST.get(
            "priority",
            "Medium"
        )

        status = request.POST.get(
            "status",
            "Pending"
        )

        description = request.POST.get(
            "description",
            ""
        ).strip()


        # =================================
        # VALIDATION
        # =================================

        if not title or not customer_id or not due_date:

            messages.error(
                request,
                "Task title, customer and due date are required."
            )


            customers = Customer.objects.all()


            return render(
                request,
                "task_form.html",
                {
                    "customers": customers,
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
        # CREATE TASK
        # =================================

        Task.objects.create(

            title=title,

            customer=customer,

            task_type=task_type,

            due_date=due_date,

            due_time=(
                due_time
                if due_time
                else None
            ),

            priority=priority,

            status=status,

            description=description

        )


        messages.success(
            request,
            "Task added successfully!"
        )


        return redirect(
            "tasks"
        )


    customers = Customer.objects.all()


    return render(
        request,
        "task_form.html",
        {
            "customers": customers
        }
    )


# =========================================
# EDIT TASK
# =========================================

def edit_task(request, id):

    if not request.user.is_authenticated:
        return redirect("login")


    task = get_object_or_404(
        Task,
        id=id
    )


    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        customer_id = request.POST.get(
            "customer"
        )

        task_type = request.POST.get(
            "task_type",
            "Follow-up"
        )

        due_date = request.POST.get(
            "due_date"
        )

        due_time = request.POST.get(
            "due_time"
        )

        priority = request.POST.get(
            "priority",
            "Medium"
        )

        status = request.POST.get(
            "status",
            "Pending"
        )

        description = request.POST.get(
            "description",
            ""
        ).strip()


        # =================================
        # VALIDATION
        # =================================

        if not title or not customer_id or not due_date:

            messages.error(
                request,
                "Task title, customer and due date are required."
            )


            customers = Customer.objects.all()


            return render(
                request,
                "task_form.html",
                {
                    "task": task,
                    "customers": customers,
                }
            )


        # =================================
        # UPDATE TASK
        # =================================

        task.title = title


        task.customer = get_object_or_404(
            Customer,
            id=customer_id
        )


        task.task_type = task_type

        task.due_date = due_date


        task.due_time = (
            due_time
            if due_time
            else None
        )


        task.priority = priority

        task.status = status

        task.description = description


        task.save()


        messages.success(
            request,
            "Task updated successfully!"
        )


        return redirect(
            "tasks"
        )


    customers = Customer.objects.all()


    return render(
        request,
        "task_form.html",
        {
            "task": task,
            "customers": customers,
        }
    )


# =========================================
# DELETE TASK
# =========================================

def delete_task(request, id):

    if not request.user.is_authenticated:
        return redirect("login")


    task = get_object_or_404(
        Task,
        id=id
    )


    if request.method == "POST":

        task.delete()


        messages.success(
            request,
            "Task deleted successfully!"
        )


    return redirect(
        "tasks"
    )