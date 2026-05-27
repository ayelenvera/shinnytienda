from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from store.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('cart.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Shinny Tienda — Administración"
admin.site.site_title = "Shinny Tienda"
admin.site.index_title = "Panel de control"
