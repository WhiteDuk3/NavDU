from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from myapp.views import IndexView, ArxivView , AboutView,MuallifView,TahririyatView,TalablarView, email_handler
from myapp import views   # replace 'your_app' with the actual app name




# TEMPORARY - create admin (only use once, then remove)
from django.contrib.auth import get_user_model
from django.http import HttpResponse

def create_admin_once(request):
    User = get_user_model()
    username = "username"                     # CHANGE THIS
    email = "isfanchik1212@gmail.com"                  # CHANGE THIS
    password = "password"       # CHANGE THIS to a strong password
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        return HttpResponse("Admin created")
    return HttpResponse("Admin already exists")


urlpatterns = [
    path('debug/', views.debug_db, name='debug_db'),
    path('create-admin/', views.create_superuser, name='create_admin'),
    path('create-admin-once/', create_admin_once),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('arxiv/', ArxivView.as_view(), name='arxiv'),
    path('about/', AboutView.as_view(), name='about'),
    path('muallif/', MuallifView.as_view(), name='muallif'),
    path('tahririyat/', TahririyatView.as_view(), name='tahririryat'),
    path('talablar/', TalablarView.as_view(), name='talablar'),
    path('email_handler/', email_handler)
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




