from django.db import models


class Services(models.Model):
    image = models.ImageField(upload_to='service_image', null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title
