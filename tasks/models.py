from django.db import models
from customers.models import Customer


class Task(models.Model):

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    TASK_TYPE_CHOICES = [
        ('Call', 'Call'),
        ('Meeting', 'Meeting'),
        ('Email', 'Email'),
        ('Follow-up', 'Follow-up'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=150)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    task_type = models.CharField(
        max_length=30,
        choices=TASK_TYPE_CHOICES,
        default='Follow-up'
    )

    due_date = models.DateField()

    due_time = models.TimeField(
        null=True,
        blank=True
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title