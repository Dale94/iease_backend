from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls import handler400, handler404
from django.contrib import admin
from accounts.views import *
from django.conf import settings


password_token = settings.CUSTOM_PASSWORD_TOKEN

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(f'{password_token}/auth/', include('djoser.urls')),
    path(f'{password_token}/auth/', include('djoser.urls.jwt'), name="jwt"),
    path(f'{password_token}/auth/', include("djoser.urls.authtoken")),
    path(f'{password_token}/auth/', include('djoser.social.urls')),
    #  path(f'{password_token}/auth/users/reset_username/', reset_username_view, name='reset_username'),
    path(f'{password_token}/department/', include('accounts.urls')),

    ##################### activate #####################################
    path('activate/<str:uid>/<str:token>', activate_account),
    path('email/reset/confirm/<str:uid>/<str:token>', reset_email),
    path('password/reset/confirm/<str:uid>/<str:token>', reset_password),

    ################### custom Update view ##################################
    path(f'{password_token}/update_profile/<int:pk>/', UpdateProfileView.as_view()),

    ############################ apps ####################3
    path(f'{password_token}/que/', include('queuing_app.urls')),
    path(f'{password_token}/budget/', include('budget_app.urls'))
]

# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
handler400 = 'accounts.views.bad_request'
# handler401 = 'accounts.views.unauthorized'
handler404 = 'accounts.views.page_not_found'
