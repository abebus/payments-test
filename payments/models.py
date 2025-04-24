from __future__ import annotations
# type: ignore 
import json

from django.db import models
from django_celery_beat.models import ClockedSchedule, PeriodicTask


class Invoice(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает оплату"
        PAID = "paid", "Оплачен"
        EXPIRED = "expired", "Просрочен"

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self) -> str:
        return f"Invoice #{self.id} — {self.amount}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.status == self.Status.PENDING:
            self._schedule_expiration_task()

    def _schedule_expiration_task(self) -> None:
        schedule, _ = ClockedSchedule.objects.get_or_create(clocked_time=self.due_date)

        task_name = f"expire-invoice-{self.pk}"

        PeriodicTask.objects.filter(name=task_name).delete()

        PeriodicTask.objects.create(
            name=task_name,
            task="payments.tasks.expire_invoice",
            clocked=schedule,
            one_off=True,
            args=json.dumps([self.pk]),
        )


class PaymentAttempt(models.Model):
    class Result(models.TextChoices):
        SUCCESS = "success", "Успешно"
        INSUFFICIENT_FUNDS = "insufficient", "Недостаточно средств"
        DECLINED = "declined", "Отказ"

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.CharField(
        max_length=20,
        choices=Result.choices,
        blank=True,
    )

    def save(self, *args, **kwargs) -> None:
        invoice = self.invoice
        if invoice.status == Invoice.Status.EXPIRED:
            self.result = self.Result.DECLINED
        elif invoice.status != Invoice.Status.PENDING:
            self.result = self.Result.DECLINED
        elif self.amount < invoice.amount:
            self.result = self.Result.INSUFFICIENT_FUNDS
        else:
            self.result = self.Result.SUCCESS
            invoice.status = Invoice.Status.PAID
            invoice.save()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Payment attempt #{self.id}"
