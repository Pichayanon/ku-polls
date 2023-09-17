from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='polls:index', permanent=True)),
    path('polls/', include('polls.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('admin/', admin.site.urls),
]
