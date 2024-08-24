from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PDFDocument
import PyPDF2

@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST' and request.FILES['file']:
        pdf_file = request.FILES['file']
        pdf_doc = PDFDocument(file=pdf_file)
        pdf_doc.save()

        # Leer y procesar el archivo PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()

        return JsonResponse({'text': text})

    return JsonResponse({'error': 'No se ha enviado un archivo PDF'}, status=400)
