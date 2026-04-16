from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.static import serve

def logout_view(request):
    auth_logout(request)
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='cadastros/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', include('cadastros.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]