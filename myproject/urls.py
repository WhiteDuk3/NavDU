from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from myapp.views import IndexView, ArxivView , AboutView,MuallifView,TahririyatView,TalablarView, email_handler
from myapp import views   # replace 'your_app' with the actual app name




# TEMPORARY - create admin (only use once, then remove)
from django.contrib.auth import get_user_model
from django.http import HttpResponse




urlpatterns = [
    path('debug/media/', views.list_media, name='list_media'),
    path('debug/', views.debug_db, name='debug_db'),
    path('list-media/', views.list_media, name='list_media'),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('arxiv/', ArxivView.as_view(), name='arxiv'),
    path('about/', AboutView.as_view(), name='about'),
    path('muallif/', MuallifView.as_view(), name='muallif'),
    path('tahririyat/', TahririyatView.as_view(), name='tahririryat'),
    path('talablar/', TalablarView.as_view(), name='talablar'),
    path('email_handler/', email_handler)
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








