from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import PaymentAttempt, Invoice
# Register your models here.


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(ModelAdmin):
    pass


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    pass
