from django.db import models
from django.core.validators import FileExtensionValidator

from apps.users.models import User
from apps.designers.models import Designer
from apps.services.models import Services


class Package(models.Model):
    CHOICE_TAGS = (('standard', 'Стандарт'), ('comfort', 'Комфорт'),
                   ('premium', 'Премиум'))

    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.CharField(null=True, blank=True, max_length=20)
    tag = models.CharField(choices=CHOICE_TAGS, null=True, blank=True, max_length=255)

    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'

    def __str__(self):
        return f'{self.title}'


class Company(models.Model):
    image = models.ImageField(upload_to='company_image')
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=255)
    about = models.TextField()
    phone_number_1 = models.CharField(max_length=16)
    phone_number_2 = models.CharField(max_length=16, null=True, blank=True)
    phone_number_3 = models.CharField(max_length=16, null=True, blank=True)
    email_1 = models.EmailField()
    email_2 = models.EmailField(null=True, blank=True)
    email_3 = models.EmailField(null=True, blank=True)
    social_media_1 = models.URLField(null=True, blank=True)
    social_media_2 = models.URLField(null=True, blank=True)
    social_media_3 = models.URLField(null=True, blank=True)
    social_media_4 = models.URLField(null=True, blank=True)
    address = models.CharField(null=True, max_length=255)
    site_link = models.URLField()
    packages = models.ManyToManyField(Package, related_name='packages', blank=True)
    designers = models.ManyToManyField(Designer, related_name='designers', blank=True)
    services = models.ManyToManyField(Services, related_name='company', blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def count_reviews(self):
        return self.reviews.count()

    @property
    def rating(self):
        all_stars = [review.rank for review in self.reviews.all()]
        return round(sum(all_stars) / len(all_stars), 1) if len(all_stars) > 0 else 0

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class FavoriteCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# company photos
class CompanyGallery(models.Model):
    company = models.ForeignKey(Company, related_name='gallery', on_delete=models.CASCADE, null=True)
    image = models.ImageField(
        upload_to='company_projects/',
        blank=True, null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        ]
    )

    def __str__(self):
        return f'{self.company}'

    class Meta:
        verbose_name = 'CompanyGallery'
        verbose_name_plural = 'Galleries'
