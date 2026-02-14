from django.views.generic import TemplateView
from .models import PDFFile
from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
import os


from django.http import HttpResponse, FileResponse, Http404
from django.contrib.auth import get_user_model


from django.http import JsonResponse
from django.db import connection
from django.contrib.auth import get_user_model

from django.conf import settings


def test_save(request):
    from django.core.files.base import ContentFile
    from django.core.files.storage import default_storage
    path = default_storage.save('test.txt', ContentFile(b'hello'))
    return HttpResponse(f"Saved to {path}")

def media_status(request):
    media_root = settings.MEDIA_ROOT
    exists = os.path.exists(media_root)
    writable = os.access(media_root, os.W_OK) if exists else False
    return HttpResponse(f"MEDIA_ROOT: {media_root}<br>Exists: {exists}<br>Writable: {writable}")

def list_media(request):
    media_root = settings.MEDIA_ROOT
    if not os.path.exists(media_root):
        return JsonResponse({'error': 'Media directory does not exist'})
    files = []
    for root, dirs, filenames in os.walk(media_root):
        for f in filenames:
            full_path = os.path.join(root, f)
            relative_path = os.path.relpath(full_path, media_root)
            files.append(relative_path)
    return JsonResponse({'files': files})


def serve_media(request, file_path):
    # Security: prevent directory traversal
    safe_path = os.path.normpath(file_path).lstrip('/')
    if '..' in safe_path or safe_path.startswith('../'):
        raise Http404
    full_path = os.path.join(settings.MEDIA_ROOT, safe_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return FileResponse(open(full_path, 'rb'))
    raise Http404

def debug_db(request):
    User = get_user_model()
    user_count = User.objects.count()
    db_name = connection.settings_dict['NAME']
    return JsonResponse({
        'database': db_name,
        'user_count': user_count,
        'users': list(User.objects.values('username', 'is_superuser'))
    })



def send_email_with_attachment(subject, body, from_email, to_emails, attachment_file_path):
    email = EmailMessage(
        subject=subject,
        body="",
        from_email=from_email,
        to=to_emails,
    )
    
    with open(attachment_file_path, 'rb') as f:
        email.attach(attachment_file_path, f.read(), 'application/octet-stream')
    email.attach(content=body, mimetype='text/html')
    email.send()

def email_handler(request):
    if request.method == 'POST':
        name=request.POST.get('name', None)
        tel=request.POST.get('tel', None)
        email=request.POST.get('email', None)
        subject=request.POST.get('subject', None)
        file=request.FILES.get('file', None)
        if file:
            file_path = f"media/files/{file.name}"
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
        print(subject)
        message = render_to_string('email.html', {
            'name': name,
            'tel':tel,
            'email':email,
            'subject':subject})
        subject = f"New request from {name}"
        file_path = f"media/files/{file.name}"
        send_email_with_attachment(subject, message, 'azizbekbakhromov12@gmail.com', ['tuya.latifbobo.aket@gmail.com'], file_path)

        if os.path.exists(file_path):
            os.remove(file_path)
        return HttpResponse("Succes")
    return HttpResponse("Failed")

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_pdf_files = PDFFile.objects.all().order_by('-id')  # Ensure items are in reverse order
        context['pdf_files'] = all_pdf_files[:6]  # Get the first 6 items of the reversed queryset
        return context

class ArxivView(TemplateView):
    template_name = 'arxiv.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pdf_files'] = PDFFile.objects.all()
        return context
    


class AboutView(TemplateView):
    template_name = 'aboutus.html'

class MuallifView(TemplateView):
    template_name = 'muallif.html'


class TahririyatView(TemplateView):
    template_name = 'tahririyat.html'

class TalablarView(TemplateView):
    template_name = 'talablar.html'







