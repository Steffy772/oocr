from django.db import models
from core import utils
import hashlib
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
from docx2pdf import convert
import os
import aspose.words as aw



class ImageFileManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(models.Q(internal_reference__icontains=query) |
                                          models.Q(name__icontains=query) |
                                          models.Q(description__icontains=query)
                                          )


class ImageFile(models.Model):

    name = models.CharField("Name", max_length=100)
    internal_reference = models.CharField("Internal Reference", max_length=100, editable=False)
    description = models.TextField("Description", blank=True, null=True)
    image = models.ImageField(upload_to="OCR_image/input/", verbose_name="Input Image")
    create_at = models.DateTimeField("Create at", auto_now_add=True)
    updated_at = models.DateTimeField("Update at", auto_now=True)

    def __str__(self):
        return "{0:03d} - {1}".format(self.id, self.image)

    def execute_and_save_ocr(self):
        import time
        start_time = time.time()

        img = Image.open(self.image)
        txt = pytesseract.image_to_string(img, lang='eng')
        execution_time = time.time() - start_time
        ocr_txt = OCRText(image = self, text = txt, lang = "EN", execution_time = execution_time)
        ocr_txt.save()

        print("The image {0} was opened.".format(self.image))
        print('OCR: \n{0}\n'.format(txt))
        print('Execution Time: {0}'.format(ocr_txt.execution_time))

        return ocr_txt

    """
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('course_details', args=[], kwargs={'slug': self.slug})
    """

    def save(self, *args, **kwargs):

        if not self.internal_reference:
            random_value = utils.random_value_generator(size=20)
            while ImageFile.objects.filter(internal_reference=random_value).exists():
                random_value = utils.random_value_generator(size=20)
            hash_value = hashlib.md5(bytes(str(self.id) + str(random_value), 'utf-8'))
            self.internal_reference = hash_value.hexdigest()
        super(ImageFile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "ImageFile"
        verbose_name_plural = "ImageFiles"
        ordering = ['id']

    objects = ImageFileManager()


class PdfFile(models.Model):

    name = models.CharField("Name", max_length=100)
    pdf = models.FileField(upload_to="OCR_image/pdf/", verbose_name="Input Image")
    create_at = models.DateTimeField("Create at", auto_now_add=True)
    updated_at = models.DateTimeField("Update at", auto_now=True)

    def __str__(self):
        return "{0:03d} - {1}".format(self.id, self.pdf)

    def execute_pdf_ocr(self):
        filepaths = self.pdf
        ext = os.path.splitext('media/' + str(filepaths))[-1].lower()
        print(ext)
        if ext == ".docx" or ".doc":
            doc = aw.Document('media/' + str(filepaths))
            docs = doc.save("prakash.pdf")
            reader = PdfReader("prakash.pdf")
            number_of_pages = len(reader.pages)
            empty = ""
            for i in range(0,number_of_pages):
                page = reader.pages[i]
                text = page.extract_text()
                empty = empty + text
            ocr_txt = PdfOcrText(pdf = self, text = empty)
            ocr_txt.save()
            return ocr_txt    
        elif ext == ".pdf":   
            reader = PdfReader(filepaths)
            number_of_pages = len(reader.pages)
            empty = ""
            for i in range(0,number_of_pages):
                page = reader.pages[i]
                text = page.extract_text()
                empty = empty + text
            ocr_txt = PdfOcrText(pdf = self, text = empty)
            ocr_txt.save()
            return ocr_txt

        else:
            print("unknown format")


class PdfOcrText(models.Model):
     text = models.TextField("PdfOcrText", blank=True)
     pdf = models.ForeignKey('PdfFile', on_delete=models.CASCADE)

     def __str__(self):
        return "{0:03d} - {1}".format(self.id, self.text)





class OCRText(models.Model):
    text = models.TextField("OCR text", blank=True)
    lang = models.TextField("Language", default="EN")
    execution_time = models.IntegerField("Execution Time", editable=False, null=True);
    image = models.ForeignKey('ImageFile', on_delete=models.CASCADE)
    create_at = models.DateTimeField("Create at", auto_now_add=True)
    updated_at = models.DateTimeField("Update at", auto_now=True)

    def __str__(self):
        return "{0:03d} - {1}".format(self.id, self.image.internal_reference)

    class Meta:
        verbose_name = "OCRText"
        verbose_name_plural = "OCRTexts"
        ordering = ['id']
