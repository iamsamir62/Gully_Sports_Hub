
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from gullyapp.urls import websocket_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('gullyapp.urls')),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
