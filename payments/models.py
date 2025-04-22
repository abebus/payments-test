from django.db import models

# Create your models here.


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
        return f"Invoice #{self.id} — {self.amount} ₽"


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

    def __str__(self) -> str:
        return f"Попытка оплаты #{self.id}"
