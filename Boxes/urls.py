from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Boxes.utils import schema_view

api_patterns = [
    path('items/', include('items.urls')),
    path('users/', include('users.urls')),
    path('reviews/', include('reviews.urls')),
    path('carts/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(api_patterns)),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
