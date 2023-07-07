from django.db import models
from apps.users.models import User
from apps.companies.models import Company
from apps.designers.models import Designer


class CompanyReview(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rank = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, related_name='reviews')
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.author is not None:
            return f'Review by {self.author.username} for Company: {self.company.title}'
        return self.text


class DesignerReview(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rank = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, blank=True, null=True, related_name='comment')
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.author is not None:
            return f'Review by {self.author.username} for Designer: {self.designer.name}'
        return self.text
