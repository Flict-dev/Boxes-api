from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ReadOnlyModelViewSet

from items.filters import ItemFilter
from items.models import Item
from items.serializers import ItemSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache


class ItemPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page-size'
    max_page_size = 4


ITEM_CACHE_KEY = 'item_cache'
ITEM_CACHE_TTL = 60 * 5


class ItemViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = ItemPageNumberPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering = ['weight', 'price']
    filterset_fields = ['weight', 'price']
    filterset_class = ItemFilter

    def list(self, request, *args, **kwargs):
        response_cache = cache.get(ITEM_CACHE_KEY)
        if response_cache:
            return Response(json.loads(response_cache))
        response = super(ItemViewSet, self).list(request, *args, **kwargs)
        cache.set(ITEM_CACHE_KEY, json.dumps(response.data), ITEM_CACHE_TTL)
        return response
