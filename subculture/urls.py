from django.conf.urls import url, include
from django.contrib import admin
import pullhold.views as views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^pullhold/', include('pullhold.urls')),
    url(r'^admin/', admin.site.urls),
    # url(r'^$', TemplateView.as_view(template_name='pullhold/index.html'),
    #     name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
