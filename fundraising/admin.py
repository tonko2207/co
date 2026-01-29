from django.contrib import admin
from .models import Fundraiser, Donation


@admin.register(Fundraiser)
class FundraiserAdmin(admin.ModelAdmin):
    list_display = ("title", "goal_amount", "collected_amount", "is_active", "created_at", "ends_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "collected_amount")


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("fundraiser", "amount", "donor_name", "created_at")
    list_filter = ("fundraiser",)
    search_fields = ("fundraiser__title", "donor_name")
    readonly_fields = ("created_at",)
