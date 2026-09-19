from django.db import models
from customers.models import Customer
from leads.models import Lead


class Deal(models.Model):

    STAGE_CHOICES = [
        ('New', 'New'),
        ('Proposal', 'Proposal'),
        ('Negotiation', 'Negotiation'),
        ('Won', 'Won'),
        ('Lost', 'Lost'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Won', 'Won'),
        ('Lost', 'Lost'),
    ]

    deal_name = models.CharField(max_length=150)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='deals'
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deals'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    stage = models.CharField(
        max_length=30,
        choices=STAGE_CHOICES,
        default='New'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    expected_close_date = models.DateField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.deal_name