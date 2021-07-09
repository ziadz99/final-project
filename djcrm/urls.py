from django.conf import settings
from django.conf.urls.static import static
from leads.views import landing_page
from django.contrib import admin
from django.urls import path , include
from leads.views import landing_page , LandingPageView , DashboardView
from django.contrib.auth.views import LoginView , LogoutView , PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from main.views import ContactsIndexView, CostumersIndexView, MappingView
from django.urls import path, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('',LandingPageView.as_view(), name = 'landing-page'),
    path('leads/', include('leads.urls',namespace="leads")),
    path('agents/', include('agents.urls',namespace="agents")),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('reset_password/',PasswordResetView.as_view(),name= 'reset-password'),
    path('password-reset-done/',PasswordResetDoneView.as_view(),name= 'password_reset_done'),
    path('password-reset-complete/',PasswordResetDoneView.as_view(),name= 'password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name= 'password_reset_confirm'),
    path('contacts', ContactsIndexView, name='contacts-index'),
    path('map', MappingView, name='map'),
    path('costumers', CostumersIndexView, name='costumers-index'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)