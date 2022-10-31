from django import forms
from uploader.models import ImageFile
from uploader.models import PdfFile



class ImageFileForm(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = ('image', )



class PdfFileForm(forms.ModelForm):
    class Meta:
        model = PdfFile
        fields = ('pdf', )
