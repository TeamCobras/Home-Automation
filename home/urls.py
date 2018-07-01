from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('work', views.work),
    #path('work', TemplateView.as_view(template_name="dashboard.html"), name='newpage'),
]