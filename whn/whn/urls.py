from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from whn.settings import DEBUG, MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('info.urls')),
    path('game/', include('game.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

if DEBUG is True:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
