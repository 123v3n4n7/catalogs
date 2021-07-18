from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from .models import *
import datetime


class CatalogListView(generics.ListAPIView):
    """Возвращает список справочников"""
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        date = request.GET.get('date', None)
        if date is not None:
            # Если параметр 'date' не пустой, то выполняется проверка на корректность данных
            # и получение списка каталогов, отфильтрованных по дате
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d")
                response_data = CatalogSerializer(self.get_queryset().filter(date=date), many=True)
            except ValueError:
                return Response('Param "date" must be like YYYY-MM-DD', status=status.HTTP_400_BAD_REQUEST)
        else:
            # Получает список каталогов
            response_data = CatalogSerializer(self.get_queryset(), many=True)
        return Response(response_data.data)


class ElementListView(generics.ListAPIView):
    """Возвращает список элементов справочника"""
    queryset = Catalog.objects.all()
    serializer_class = ElementSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        catalog_name = request.GET.get('catalog_name', None)
        version = request.GET.get('version', None)
        if catalog_name is None and version is None:
            # Проверка корректности параметров. Если параметры некорректны, то возвращает сообщение об ошибке.
            return Response('Empty params catalog_name and version', status=status.HTTP_400_BAD_REQUEST)
        if version is None:
            # Если есть только параметр catalog_name, то получает последнюю версию каталога. Проверяется корректность
            # параметра, если параметр некорректен, то возвращает сообщение с ошибкой. Ищется последняя версия каталога
            # и список элементов этого каталога.
            try:
                queryset = self.get_queryset().prefetch_related('element_set')
                last_version = max(queryset.filter(name=catalog_name).values_list('version', flat=True))
                catalog = queryset.filter(name=catalog_name).filter(version=last_version)[0]
                elements = catalog.element_set.all()
            except Exception as ex:
                return Response('"catalog_name" param is not correct', status=status.HTTP_400_BAD_REQUEST)
            data = ElementSerializer(elements, many=True)
            return Response(data.data, status=status.HTTP_200_OK)
        else:
            # Если есть оба параметра 'catalog_name' и 'version', то проверяется их корректность, если параметры
            # некорректны, то возращается ошибка. Выполняется поиск каталога по указанным параметрам,
            # затем берутся элементы этого каталога.
            try:
                queryset = self.get_queryset().prefetch_related('element_set')
                catalog = queryset.filter(name=catalog_name).filter(version=version)[0]
                elements = catalog.element_set.all()
            except Exception as ex:
                return Response('"version" or "catalog_name" params is not correct', status=status.HTTP_400_BAD_REQUEST)
            data = ElementSerializer(elements, many=True)
            return Response(data.data, status=status.HTTP_200_OK)
