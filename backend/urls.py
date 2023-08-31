
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('doctor/', include('doctor.urls')),
    path('booking/', include('booking.urls')),
    path('review/', include('review.urls')),
    path('report/', include('report.urls')),
    path('chat/', include('chat.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)