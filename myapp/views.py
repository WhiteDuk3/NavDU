import os
from django.views.generic import TemplateView
from django.shortcuts import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import FileResponse, Http404
from django.conf import settings
from .models import PDFFile
from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages
from django.urls import reverse

from django.shortcuts import render, get_object_or_404

def about(request):
    popular_articles = PDFFile.objects.all().order_by('-date')[:6]
    return render(request, 'about.html', {'popular_articles': popular_articles})
def article_preview(request, pdf_id):
    article = get_object_or_404(PDFFile, id=pdf_id)
    # Increment view count
    # article.view_count += 1
    # article.save(update_fields=['view_count'])
    
    # Get related articles (same category, exclude current)
    related_articles = PDFFile.objects.filter(category=article.category).exclude(id=article.id).order_by('-date')[:3]
    
    return render(request, 'article_preview.html', {
        'article': article,
        'related_articles': related_articles
    })

def download_article(request, pdf_id):
    article = get_object_or_404(PDFFile, id=pdf_id)
    # article.download_count += 1
    # article.save(update_fields=['download_count'])
    return redirect(article.file.url)


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
        name = request.POST.get('name', '').strip()
        tel = request.POST.get('tel', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        uploaded_file = request.FILES.get('file')

        # Basic validation
        if not name or not tel or not email or not subject:
            messages.error(request, "Barcha majburiy maydonlarni toʻldiring.")
            return redirect('muallif')  # assuming you have a URL name for this page

        file_path = None
        if uploaded_file:
            # Limit file size (optional) – e.g., 10MB
            if uploaded_file.size > 10 * 1024 * 1024:
                messages.error(request, "Fayl hajmi 10MB dan oshmasligi kerak.")
                return redirect('muallif')

            # Save temporarily
            files_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
            os.makedirs(files_dir, exist_ok=True)
            file_path = os.path.join(files_dir, uploaded_file.name)
            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

        # Prepare email
        message = render_to_string('email.html', {
            'name': name,
            'tel': tel,
            'email': email,
            'subject': subject,
        })
        email_subject = f"Yangi murojaat: {subject}"
        from_email = settings.EMAIL_HOST_USER
        to_emails = ['isfanchik1212@gmail.com']  # CHANGE THIS to your recipient email

        try:
            send_email_with_attachment(email_subject, message, from_email, to_emails, file_path)
            messages.success(request, "Murojaatingiz muvaffaqiyatli yuborildi. Tez orada siz bilan bogʻlanamiz.")
        except Exception as e:
            # Log the error (you can use print or logging)
            print(f"Email error: {e}")
            messages.error(request, "Xatolik yuz berdi. Iltimos, keyinroq urinib koʻring yoki administrator bilan bogʻlaning.")
        finally:
            # Clean up temp file
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

        return redirect('muallif')  # redirect back to the form page

    return HttpResponse("Notoʻgʻri soʻrov", status=400)


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
        # Get all PDFs, order by date
        all_pdfs = PDFFile.objects.all().order_by('-date')
        
        # Filtering
        search_query = self.request.GET.get('q', '')
        category = self.request.GET.get('category', '')
        year = self.request.GET.get('year', '')
        
        if search_query:
            all_pdfs = all_pdfs.filter(name__icontains=search_query) | \
                       all_pdfs.filter(abstract__icontains=search_query) | \
                       all_pdfs.filter(authors__icontains=search_query)
        if category and category != 'all':
            all_pdfs = all_pdfs.filter(category__iexact=category)
        if year and year != 'all':
            all_pdfs = all_pdfs.filter(date__year=year)
        
        # Get unique categories and years for filter dropdowns
        categories = PDFFile.objects.exclude(category__isnull=True).exclude(category='').values_list('category', flat=True).distinct().order_by('category')
        years = PDFFile.objects.exclude(date__isnull=True).dates('date', 'year').distinct()
        
        context['pdf_files'] = all_pdfs
        context['recent_pdfs'] = PDFFile.objects.all().order_by('-date')[:6]
        context['categories'] = categories
        context['years'] = [d.year for d in years]
        context['selected_category'] = category
        context['selected_year'] = year
        context['search_query'] = search_query
        return context

class AboutView(TemplateView):
    template_name = 'aboutus.html'


class MuallifView(TemplateView):
    template_name = 'muallif.html'


class TahririyatView(TemplateView):
    template_name = 'tahririyat.html'


class TalablarView(TemplateView):
    template_name = 'talablar.html'












