from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django_otp.plugins.otp_totp.models import TOTPDevice


class EnforceVet2FAMiddleware(MiddlewareMixin):
    VET_GROUP_NAME = "Weterynarz"

    def process_request(self, request):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return None

        # Only vets
        if not user.groups.filter(name=self.VET_GROUP_NAME).exists():
            return None

        # Already OTP verified -> OK
        is_verified = getattr(user, "is_verified", None)
        verified = is_verified() if callable(is_verified) else False
        if verified:
            return None

        # Allow login/logout and 2FA pages to prevent redirect loops
        allowed_prefixes = (
            reverse("login"),
            reverse("logout"),
            reverse("twofa_setup"),
            reverse("twofa_verify"),
        )

        if any(request.path.startswith(p) for p in allowed_prefixes):
            return None

        # If vet has confirmed device -> go verify, else go setup
        if TOTPDevice.objects.filter(user=user, confirmed=True).exists():
            return redirect(f"{reverse('twofa_verify')}?next={request.path}")

        return redirect(reverse("twofa_setup"))
