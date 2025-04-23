from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.sites import UnfoldAdminSite

from .admin import InvoiceAdminMixin, PaymentAttemptAdminMixin
from .models import Invoice, PaymentAttempt


class NewUnfoldAdminSite(UnfoldAdminSite):
    pass


unfold_admin_site = NewUnfoldAdminSite(name="unfold")


@admin.register(PaymentAttempt, site=unfold_admin_site)
class PaymentAttemptUnfoldAdmin(UnfoldModelAdmin, PaymentAttemptAdminMixin):
    pass


@admin.register(Invoice, site=unfold_admin_site)
class InvoiceUnfoldAdmin(UnfoldModelAdmin, InvoiceAdminMixin):
    pass
