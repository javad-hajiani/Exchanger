from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from web.views import *

urlpatterns = [
    path('', redirect_view),
    path('home/', home),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)