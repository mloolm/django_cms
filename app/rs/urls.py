from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls.i18n import i18n_patterns
from two_factor.urls import urlpatterns as tf_urls
from .admin_views import set_admin_language

handler404 = 'django.views.defaults.page_not_found'
handler400 = 'django.views.defaults.bad_request'
handler403 = 'django.views.defaults.permission_denied'
handler500 = 'django.views.defaults.server_error'
urlpatterns = [
    path('upload-image/', views.upload_image, name='upload_image'),
    path('admin-gallery/', views.gallery_view, name='gallery'),
    path('api/img-list/', views.file_list, name='img_list'),
    path('admin-delete-file/<str:file_name>/', views.delete_file, name='delete_file'),
    path('admin/', admin.site.urls),
    path("", include(tf_urls)),  # Пути для авторизации 2FA,
    path('set-admin-lang/', set_admin_language, name='admin-set-lang'),
]

# Adding routes with a language prefix
urlpatterns += i18n_patterns(
    path('', include('website.urls')),
    prefix_default_language=False
)

urlpatterns += i18n_patterns(
    path('donations/', include('donations.urls')),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
