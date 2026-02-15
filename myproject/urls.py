from django.contrib import admin
from django.urls import path, re_path
from myapp.views import (
    IndexView, ArxivView, AboutView, MuallifView,
    TahririyatView, TalablarView, email_handler, serve_media
)
from myapp import views

urlpatterns = [
    path('article/<int:pdf_id>/', views.article_preview, name='article_preview'),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('arxiv/', ArxivView.as_view(), name='arxiv'),
    path('about/', AboutView.as_view(), name='about'),
    path('muallif/', MuallifView.as_view(), name='muallif'),
    path('tahririyat/', TahririyatView.as_view(), name='tahririryat'),
    path('talablar/', TalablarView.as_view(), name='talablar'),
    path('email_handler/', email_handler, name='email_handler'),
    re_path(r'^media/(?P<file_path>.*)$', serve_media, name='serve_media'),
]





