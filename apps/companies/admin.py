from django.contrib import admin

from .models import Company, CompanyGallery, Package, FavoriteCompany


admin.site.register(Company)
admin.site.register(CompanyGallery)
admin.site.register(Package)
admin.site.register(FavoriteCompany)
