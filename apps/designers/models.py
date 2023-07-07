from django.db import models

from apps.users.models import User


class Designer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='designer_media')
    work_EXP = models.CharField(max_length=50, null=True, blank=True)
    occupation = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    instagram = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def company_title(self):
        return [company.title for company in self.designers.all()]

    @property
    def rating(self):
        stars = [reviews.rank for reviews in self.comment.all()]
        return round(sum(stars) / len(stars), 1) if len(stars) > 0 else 0

    @property
    def count_reviews(self):
        return self.comment.count()

    class Meta:
        verbose_name = 'Designer'
        verbose_name_plural = 'Designers'


class FavoriteDesigner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


class DesignerGallery(models.Model):
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='designer_gallery/', verbose_name='Images')
    about = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Designer_Gallery'
        verbose_name_plural = 'Designer_Galleries'
