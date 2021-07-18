from django.contrib import admin
from .models import Catalog, Element


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_name', 'description', 'version', 'date']
    search_fields = ['name', 'id']
    list_filter = ['name', 'version']


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ['id', 'catalog_id', 'element_code', 'element_value']
    search_fields = ['element_code']
    list_filter = ['catalog_id', 'element_code']