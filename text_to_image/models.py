from django.db import models

# Create your models here.


class GeneratedImage(models.Model):
    text = models.CharField(max_length=100)
    image = models.ImageField(upload_to='generated_images/')

    def __str__(self):
        return self.text