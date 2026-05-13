from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve as static_serve
from escolta_system.compress_view import compress_photos_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('_compress/', compress_photos_view),  # TEMPORÁRIO — remover após uso
    path('login/', auth_views.LoginView.as_view(template_name='cadastros/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('cadastros.urls')),
]

# Serve /media/ em DEV e PROD.
# Em DEV: helper static() padrão do Django.
# Em PROD: django.views.static.serve (necessário pq Railway não tem nginx/S3 dedicado).
#   Risco de perf/security é aceitável pro volume de uploads deste sistema.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
    ]
