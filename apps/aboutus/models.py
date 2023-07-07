from django.db import models


class AboutUs(models.Model):
    image = models.ImageField(upload_to='aboutus/', verbose_name='image', default='aboutus/obi.jpg')
    description = models.TextField()
    phone_number = models.CharField(max_length=20)
    instagram = models.URLField()
    mail = models.EmailField()
    address = models.CharField(null=True, max_length=255)
