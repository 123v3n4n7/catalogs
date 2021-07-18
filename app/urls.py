from django.urls import path

from .views import *

app_name = 'App_'
urlpatterns = [
    path("", CatalogListView.as_view(), name='catalog_view'),
    path("elements/", ElementListView.as_view(), name='elements_list_view')
]