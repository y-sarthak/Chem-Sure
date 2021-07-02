from django.urls import path
from .views import image_upload_view, Analysis
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('image_upload', image_upload_view, name = 'image_upload'),
    path('analysis/<int:id>',Analysis,name="employee_update")

]
  
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)