from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 4


class OrderViewSet(GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = OrderLimitOffsetPagination
    queryset = Order.objects.prefetch_related('cart')
    throttle_scope = 'orders'

    def list(self, request):
        queryset = Order.objects.prefetch_related('cart__cart_items__item').filter(recipient=request.user)
        objects = self.paginate_queryset(queryset)
        serializer = OrderSerializer(objects, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk):
        try:
            order = Order.objects.prefetch_related('cart__cart_items__item').get(id=pk)
        except Order.DoesNotExist:
            raise Http404
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        if order.status == 'created':
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            message = 'Вы не можете редактировать заказ в обработке/доставленный заказ/отмененный заказ'
            return Response({"data": f"{message}"}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        if order.status == 'created':
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = 'Вы не можете редактировать заказ в обработке/доставленный заказ/отмененный заказ'
            return Response({"data": f"{message}"}, status=status.HTTP_400_BAD_REQUEST)
