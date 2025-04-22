from __future__ import annotations

from celery import shared_task
from django.utils import timezone

from .models import Invoice


@shared_task
def expire_invoice(invoice_id: int) -> None:
    invoice = Invoice.objects.filter(
        id=invoice_id, status=Invoice.Status.PENDING
    ).first()
    if invoice and invoice.due_date <= timezone.now():
        invoice.status = Invoice.Status.EXPIRED
        invoice.save()
