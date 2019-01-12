from django.urls import path
from django.views.generic import RedirectView

from web.views import *

urlpatterns = [
    path('', redirect_view),
    path('home/', home),
]