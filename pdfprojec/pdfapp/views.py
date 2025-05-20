from django.shortcuts import render, redirect
from .models import PDFDocument
from .forms import PDFUploadForm
from django.core.paginator import Paginator

def display_pdfs(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    pdfs = PDFDocument.objects.all().order_by('-uploaded_at')

    if query:
        pdfs = pdfs.filter(title__icontains=query)

    if category:
        pdfs = pdfs.filter(category__iexact=category)

    paginator = Paginator(pdfs, 6)  # 6 PDFs per page
    page_number = request.GET.get('page')
    page_pdfs = paginator.get_page(page_number)

    form = PDFUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('display_pdfs')

    return render(request, 'pdfapp/display.html', {
        'pdfs': page_pdfs,
        'form': form
    })
