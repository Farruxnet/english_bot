from django.db import models

class Words(models.Model):
    oz = models.CharField(max_length = 255, verbose_name = "O'zbek")
    en = models.CharField(max_length = 255, verbose_name = "Ingliz")

    def __str__(self):
        return self.oz
        
    class Meta:
        verbose_name = "So'z"
        verbose_name_plural = "So'zlar"
