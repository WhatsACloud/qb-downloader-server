from django.urls import path
from . import views

urlpatterns = [
    path('callback/', views.index, name='callback'),
    path('zipDownload/', views.zipDownload, name='zipDownload'),
    path('launch/', views.launch, name='launch'),
]
