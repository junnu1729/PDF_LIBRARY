from django.db import models
from pdf2image import convert_from_path
import os
from django.conf import settings
from django.utils import timezone


class PDFDocument(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)
    pdf_file = models.FileField(upload_to='pdfs/')
    thumbnail = models.ImageField(upload_to='pdf_thumbnails/', blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.PositiveIntegerField(blank=True, null=True)  # in bytes

    def save(self, *args, **kwargs):
        # First save the PDF
        super().save(*args, **kwargs)

        # Save file size if not already set
        if self.pdf_file and not self.file_size:
            self.file_size = self.pdf_file.size
            super().save(update_fields=['file_size'])

        # Generate thumbnail if not already present
        if self.pdf_file and not self.thumbnail:
            try:
                # Windows: Path to Poppler bin folder
                poppler_path = r'C:\Users\USER\Downloads\Release-24.08.0-0 (1)\poppler-24.08.0\Library\bin'

                print("Generating thumbnail...")
                pages = convert_from_path(
                    self.pdf_file.path,
                    first_page=1,
                    last_page=1,
                    poppler_path=poppler_path
                )

                if pages:
                    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_thumbnails')
                    os.makedirs(thumbnail_dir, exist_ok=True)

                    thumb_filename = f'{self.pk}_thumb.jpg'
                    thumb_full_path = os.path.join(thumbnail_dir, thumb_filename)

                    # Save the first page as thumbnail
                    pages[0].save(thumb_full_path, 'JPEG')
                    print(f"Thumbnail saved to {thumb_full_path}")

                    self.thumbnail.name = f'pdf_thumbnails/{thumb_filename}'
                    super().save(update_fields=['thumbnail'])

            except Exception as e:
                print(f"Error generating thumbnail: {e}")

    def __str__(self):
        return self.title
