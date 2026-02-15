import os
from django.views.generic import TemplateView
from django.shortcuts import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import FileResponse, Http404
from django.conf import settings
from .models import PDFFile

from django.shortcuts import render, get_object_or_404


def article_preview(request, pdf_id):
    article = get_object_or_404(PDFFile, id=pdf_id)
    return render(request, 'article_preview.html', {'article': article})

# ---------- Media serving ----------
def serve_media(request, file_path):
    """Serve media files securely (prevent directory traversal)."""
    safe_path = os.path.normpath(file_path).lstrip('/')
    if '..' in safe_path or safe_path.startswith('../'):
        raise Http404
    full_path = os.path.join(settings.MEDIA_ROOT, safe_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return FileResponse(open(full_path, 'rb'))
    raise Http404


# ---------- Email helpers ----------
def send_email_with_attachment(subject, body, from_email, to_emails, attachment_file_path):
    email = EmailMessage(
        subject=subject,
        body="",
        from_email=from_email,
        to=to_emails,
    )
    # Attach file
    with open(attachment_file_path, 'rb') as f:
        email.attach(os.path.basename(attachment_file_path), f.read(), 'application/octet-stream')
    # Attach HTML body
    email.attach(content=body, mimetype='text/html')
    email.send()


def email_handler(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        tel = request.POST.get('tel', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        file = request.FILES.get('file')

        # Temporary directory for uploaded files
        files_dir = os.path.join(settings.MEDIA_ROOT, 'files')
        os.makedirs(files_dir, exist_ok=True)

        file_path = None
        if file:
            file_path = os.path.join(files_dir, file.name)
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

        # Render email body
        message = render_to_string('email.html', {
            'name': name,
            'tel': tel,
            'email': email,
            'subject': subject,
        })
        email_subject = f"New request from {name}"
        from_email = settings.EMAIL_HOST_USER  # or a default
        to_emails = ['tuya.latifbobo.aket@gmail.com']  # consider moving to settings

        send_email_with_attachment(email_subject, message, from_email, to_emails, file_path)

        # Clean up temporary file
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        return HttpResponse("Success")
    return HttpResponse("Failed")


# ---------- Page views ----------
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_pdfs = PDFFile.objects.all().order_by('-id')
        context['pdf_files'] = all_pdfs[:6]
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

