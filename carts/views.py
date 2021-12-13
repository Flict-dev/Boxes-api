from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from carts.models import Cart, CartItem
from carts.serializers import CartSerializer, CartItemSerializer


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = request.user.current_cart
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.GenericViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_obj(self, pk):
        try:
            obj = CartItem.objects.get(id=pk)
            return obj
        except ObjectDoesNotExist:
            raise Http404

    def get_queryset(self):
        cart = self.request.user.current_cart
        queryset = CartItem.objects.filter(cart=cart)
        return queryset

    def retrieve(self, request, pk=None):
        try:
            obj = CartItem.objects.select_related('item').get(id=pk)
            serializer = CartItemSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        try:
            cart = request.user.current_cart
            queryset = CartItem.objects.select_related('item').filter(cart=cart)
            objects = self.paginate_queryset(queryset)
            serializer = CartItemSerializer(objects, many=True)
            return self.get_paginated_response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        cart_item = CartItemSerializer(data=request.data, context={'request': request})
        if cart_item.is_valid():
            cart_item.save()
            return Response(cart_item.data, status=status.HTTP_201_CREATED)
        else:
            return Response(cart_item.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        obj = self.get_obj(pk)
        serializer = CartItemSerializer(obj, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        obj = self.get_obj(pk)
        serializer = CartItemSerializer(obj, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        obj = self.get_obj(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
