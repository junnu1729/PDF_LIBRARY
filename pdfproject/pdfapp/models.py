from django.db import models
from django.utils import timezone
from pdf2image import convert_from_path
from django.core.files.base import ContentFile
from io import BytesIO
import tempfile
import os

class PDFDocument(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)
    
    pdf_file = models.FileField(upload_to='pdfs/')
    thumbnail = models.ImageField(upload_to='pdf_thumbnails/', blank=True, null=True)
    
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

        
        if self.pdf_file and not self.file_size:
            self.file_size = self.pdf_file.size
            super().save(update_fields=['file_size'])

        
        if self.pdf_file and not self.thumbnail:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
                    tmp_pdf.write(self.pdf_file.read())
                    tmp_pdf.flush()

                    
                    poppler_path = r'C:\Users\USER\Downloads\Release-24.08.0-0 (1)\poppler-24.08.0\Library\bin'

                    pages = convert_from_path(
                        tmp_pdf.name,
                        first_page=1,
                        last_page=1,
                        poppler_path=poppler_path
                    )

                    if pages:
                        thumb_io = BytesIO()
                        pages[0].save(thumb_io, format='JPEG')
                        thumb_name = f'{self.pk}_thumb.jpg'

                        self.thumbnail.save(thumb_name, ContentFile(thumb_io.getvalue()), save=False)
                        super().save(update_fields=['thumbnail'])

                os.unlink(tmp_pdf.name)

            except Exception as e:
                print(f"Thumbnail generation error: {e}")

    def __str__(self):
        return self.title