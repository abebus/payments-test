from django import forms
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Invoice, PaymentAttempt

# Register your models here.


class PaymentAttemptForm(forms.ModelForm):
    class Meta:
        model = PaymentAttempt
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["invoice"].queryset = Invoice.objects.filter(
            status=Invoice.Status.PENDING
        )


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(ModelAdmin):
    __color_map: dict[tuple[str, str], str] = {
        PaymentAttempt.Result.SUCCESS: "green",
        PaymentAttempt.Result.INSUFFICIENT_FUNDS: "orange",
        PaymentAttempt.Result.DECLINED: "red",
    }

    list_display: tuple[str, ...] = (
        "id",
        "invoice",
        "amount",
        "status_colored",
        "created_at",
    )
    list_filter: tuple[str] = ("result",)
    form: PaymentAttemptForm = PaymentAttemptForm

    @admin.display(description="Результат")
    def status_colored(self, obj: PaymentAttempt) -> str:
        return format_html(
            '<b style="color: {};">{}</b>',
            self.__color_map.get(obj.result, "black"),
            obj.get_result_display(),
        )


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    __color_map: dict[tuple[str, str], str] = {
        Invoice.Status.PENDING: "orange",
        Invoice.Status.PAID: "green",
        Invoice.Status.EXPIRED: "red",
    }

    list_display: tuple[str, ...] = (
        "id",
        "amount",
        "status_colored",
        "created_at",
        "due_date",
    )
    list_filter: tuple[str] = ("status",)

    @admin.display(description="Статус")
    def status_colored(self, obj: Invoice) -> str:
        return format_html(
            '<b style="color: {};">{}</b>',
            self.__color_map.get(obj.status, "black"),
            obj.get_status_display(),
        )
