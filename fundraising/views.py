from decimal import Decimal
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Fundraiser
from .forms import FundraiserForm
from .forms import FundraiserForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404


from .models import Fundraiser, Donation


def fundraiser_list(request):
    fundraisers = Fundraiser.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "fundraising/list.html", {"fundraisers": fundraisers})


def fundraiser_detail(request, slug):
    fundraiser = get_object_or_404(Fundraiser, slug=slug, is_active=True)

    if request.method == "POST":
        amount_str = request.POST.get("amount", "").replace(",", ".").strip()
        donor_name = request.POST.get("donor_name", "").strip()

        try:
            amount = Decimal(amount_str)
        except Exception:
            amount = Decimal("0")

        if amount <= 0:
            messages.error(request, "Podaj poprawną kwotę (większą od 0).")
            return redirect("fundraising:detail", slug=fundraiser.slug)

        if fundraiser.is_ended:
            messages.error(request, "Ta zbiórka jest zakończona.")
            return redirect("fundraising:detail", slug=fundraiser.slug)

        with transaction.atomic():
            Donation.objects.create(fundraiser=fundraiser, amount=amount, donor_name=donor_name)
            Fundraiser.objects.filter(pk=fundraiser.pk).update(collected_amount=F("collected_amount") + amount)

        messages.success(request, "Dziękujemy! Wpłata została zapisana w systemie.")
        return redirect("fundraising:detail", slug=fundraiser.slug)

    return render(request, "fundraising/detail.html", {"fundraiser": fundraiser})

@staff_member_required
def fundraiser_edit(request, slug):
    fundraiser = get_object_or_404(Fundraiser, slug=slug)

    if request.method == "POST":
        form = FundraiserForm(request.POST, instance=fundraiser)
        if form.is_valid():
            form.save()
            return redirect("fundraising:detail", slug=fundraiser.slug)
    else:
        form = FundraiserForm(instance=fundraiser)

    return render(request, "fundraising/fundraiser_form.html", {
        "form": form,
        "fundraiser": fundraiser,
    })

@user_passes_test(lambda u: u.is_staff)
def create(request):
    if request.method == "POST":
        form = FundraiserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("fundraising:list")
    else:
        form = FundraiserForm()

    return render(request, "fundraising/form.html", {
        "form": form,
        "mode": "create",
    })

@user_passes_test(lambda u: u.is_staff)
def edit(request, slug):
    fundraiser = get_object_or_404(Fundraiser, slug=slug)

    if request.method == "POST":
        form = FundraiserForm(request.POST, instance=fundraiser)
        if form.is_valid():
            form.save()
            return redirect("fundraising:detail", slug=fundraiser.slug)
    else:
        form = FundraiserForm(instance=fundraiser)

    return render(request, "fundraising/form.html", {
        "form": form,
        "fundraiser": fundraiser,
        "mode": "edit",
    })
