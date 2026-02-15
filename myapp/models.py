from django.db import models

class PDFFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='pdfs/')
    image = models.ImageField(upload_to='newsniasosi/')
    category = models.CharField(max_length=50, blank=True, null=True)
    authors = models.CharField(max_length=200, blank=True, null=True)  # comma-separated
    abstract = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)  # can be HTML
    date = models.DateField(auto_now_add=True)  # automatically set on creation
    read_time = models.CharField(max_length=20, blank=True, null=True, help_text="e.g., '5 min read'")

    def __str__(self):
        return self.name
