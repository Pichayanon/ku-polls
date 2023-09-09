from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='polls', permanent=True)),
    path('polls/', include('polls.urls'), name='polls'),
    path('admin/', admin.site.urls, name='admin'),
]
