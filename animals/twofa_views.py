from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_otp import login as otp_login
from django_otp.plugins.otp_totp.models import TOTPDevice
import base64
from io import BytesIO
import qrcode



def _get_or_create_unconfirmed_device(user):
    device = TOTPDevice.objects.filter(user=user, confirmed=False).first()
    if device:
        return device
    return TOTPDevice.objects.create(user=user, name="default", confirmed=False)


@login_required
def twofa_setup(request):
    device = _get_or_create_unconfirmed_device(request.user)
    config_url = device.config_url  # otpauth://...

    # QR as base64 PNG
    qr = qrcode.make(config_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_b64 = base64.b64encode(buffer.getvalue()).decode("ascii")

    return render(request, "animals/twofa_setup.html", {
        "config_url": config_url,
        "qr_b64": qr_b64,
    })


@login_required
def twofa_verify(request):
    device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
    if not device:
        device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()

    if not device:
        return redirect("twofa_setup")

    error = None
    if request.method == "POST":
        token = (request.POST.get("token") or "").strip().replace(" ", "")
        if device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save(update_fields=["confirmed"])
            otp_login(request, device)
            next_url = request.GET.get("next") or "/animals/"
            return redirect(next_url)
        error = "Nieprawidlowy kod. Sprobuj ponownie."

    return render(request, "animals/twofa_verify.html", {"error": error})
