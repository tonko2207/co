from django.shortcuts import redirect
from django.urls import reverse

class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            completed = request.session.get("onboarding_done", False)
            onboarding_paths = [reverse("core:onboarding"), reverse("core:onboarding_complete")]

            if not completed and request.path not in onboarding_paths:
                return redirect("core:onboarding")


        return self.get_response(request)
