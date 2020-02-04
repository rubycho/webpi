"""webpi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from api.views.static import index, pi_info, pi_status, proc_cpu, proc_mem
from api.views.disk import list_dir, create_dir, download_file, upload_file, delete_item


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),

    path('sys/pi-info/', pi_info, name='pi-status'),
    path('sys/pi-status/', pi_status, name='pi-status'),
    path('sys/proc-cpu/', proc_cpu, name='proc-cpu'),
    path('sys/proc-mem/', proc_mem, name='proc-mem'),

    path('disk/download/', download_file, name='download-file'),
    path('disk/upload/', upload_file, name='upload-file'),
    path('disk/list/', list_dir, name='list-dir'),
    path('disk/create-dir/', create_dir, name='create-dir'),
    path('disk/delete/', delete_item, name='delete-item')
]
