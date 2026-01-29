from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("animals/", include("animals.urls")),
    path("aktualnosci/", include(("marketing.urls", "marketing"), namespace="marketing")),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('accounts/2fa/', include('animals.twofa_urls')),

    #path("start/", include("core.urls")),
    path("", include(("core.urls", "core"), namespace="core")),

    path("fundraising/", include("fundraising.urls", namespace="fundraising")),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
