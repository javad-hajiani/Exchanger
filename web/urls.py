from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView,
                                       PasswordResetDoneView)
from django.urls import path, include

from web.views import *

urlpatterns = [path('', redirect_view), path('home/', home_page), path('aboutus/', aboutus_page),
               path('contactus/', contactus_page), path('accounts/login/', user_login),
               path('accounts/signup/', register), path('accounts/dashboard/', dashboard_page),
               path('accounts/profile/', profile_page), path('accounts/logout/', user_logout),
               path('addcard/', add_card), path('verification/', verification_page),
               path('verifyorder/', verifyorder_page), path('coin/<coin>', coinswithamount), path('law/', law_page),
               path('updateprofile/', updateprofile), path('sendmessage/', sendmessage),
               path('grappelli/', include('grappelli.urls')),
               path('reset-password/', PasswordResetView.as_view(), name="password_reset"),
               path('reset-password/done', PasswordResetDoneView.as_view(), name="password_reset_done"),
               path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
                    name="password_reset_confirm"),
               path('reset-password/complete', PasswordResetCompleteView.as_view(), name="password_reset_complete")

               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                            document_root=settings.MEDIA_ROOT)
