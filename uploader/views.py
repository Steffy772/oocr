from django.shortcuts import render, redirect
from uploader.forms import ImageFileForm
from uploader.models import ImageFile
from uploader.forms import PdfFileForm
from uploader.models import PdfFile
from uploader.models import OCRText
from django.db.models import Q
from uploader.models import PdfOcrText
PdfOcrText


def home(request):
    data = dict()

    image_form = ImageFileForm(request.POST or None, request.FILES or None)
    if image_form.is_valid():
        image = image_form.save()
        image.execute_and_save_ocr()
        redirect('home')

    image_list = ImageFile.objects.all().order_by('-id')

    data['image_form'] = image_form
    data['image_list'] = image_list
    return render(request, "uploader/index.html", data)




def search(request):
    if request.method == "GET":
        searched = request.GET.get('searched')
        image_list = OCRText.objects.filter(text__contains=searched)
        #pdf_list = PdfOcrText.objects.filter(text__contains=searched)
        return render(request, "uploader/search.html", {'image_list':image_list})

    else:
        return render(request, "uploader/search.html")

def pdf(request):

    pdf_form = PdfFileForm(request.POST or None, request.FILES or None)
    if pdf_form.is_valid():
        pdf = pdf_form.save()
        pdf.execute_pdf_ocr()
        redirect('/pdf/')

    return render(request, "uploader/pdf.html")

def search_pdf(request):
    if request.method == "GET":
        searched = request.GET.get('searched')
        pdf_list = PdfOcrText.objects.filter(text__contains=searched)
        return render(request, "uploader/pdf_search.html", {'pdf_list':pdf_list})

    else:
        return render(request, "uploader/pdf_search.html")