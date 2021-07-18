from django.db import models
import datetime


class Catalog(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    short_name = models.CharField(max_length=50, blank=False, default='')
    description = models.TextField(blank=True, default='')
    version = models.CharField(max_length=50, default=None, editable=False)
    date = models.DateField(default=datetime.date.today())

    def save(self):
        catalog_versions_list = Catalog.objects.all().filter(name=self.name).values_list('version', flat=True)
        try:
            catalog_versions_list = [int(x.split('_')[-1]) for x in list(catalog_versions_list)]
            max_version = max(catalog_versions_list)
            self.version = str(self.name) + '_' + str(max_version + 1)
        except ValueError:
            self.version = str(self.name) + '_' + str(1)
        return super().save()

    def __str__(self):
        return self.version


class Element(models.Model):
    catalog_id = models.ForeignKey(Catalog, on_delete=models.CASCADE, null=False)
    element_code = models.CharField(max_length=20, blank=False)
    element_value = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.element_code