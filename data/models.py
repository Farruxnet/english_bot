from django.db import models
def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Ushbu fayl ketgaytmasi qabul qilinmaydi faqat txt fayl')

class Words(models.Model):
    oz = models.CharField(max_length = 255, verbose_name = "O'zbek")
    en = models.CharField(max_length = 255, verbose_name = "Ingliz")

    def __str__(self):
        return self.oz

    class Meta:
        verbose_name = "So'z"
        verbose_name_plural = "So'zlar"

class TextData(models.Model):
    file = models.FileField(upload_to='static/uploads/', validators=[validate_file_extension])

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
