from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required
def onboarding(request):
    return render(request, "core/onboarding.html")

@login_required
def onboarding_complete(request):
    if request.method == "POST":
        request.session["onboarding_done"] = True
    return redirect("/animals/")
      # albo gdzie chcesz po samouczku
