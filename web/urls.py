from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from web.views import *

urlpatterns = [
    path('', redirect_view),
    path('home/', home_page),
    path('aboutus/',aboutus_page),
    path('contactus/',contactus_page),
    path('accounts/login/',user_login),
    path('accounts/signup/', signup_page),
    path('accounts/dashboard/', dashboard_page),
    path('accounts/logout/', user_logout),
    path('law/', law_page),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)