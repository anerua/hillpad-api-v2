"""hillpad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include("account.urls")),
    path('api/academics/', include("academics.urls")),
    path('api/action/', include("action.urls")),
    path('api/notification/', include("notification.urls")),
    path('api/stats/', include("stats.urls")),
    path('.well-known/pki-validation/FD52F2748473B3ADAEAE42363F6C3B1C.txt', TemplateView.as_view(template_name="hillpad/942AA30074009A49D5046BE9F47F2E84.txt", content_type="text/plain")),
    path('staff/', include("frontend_staff.urls")),
    path('supervisor/', include("frontend_supervisor.urls")),
    path('', include("frontend.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
