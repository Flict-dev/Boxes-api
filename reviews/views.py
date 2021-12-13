from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from reviews.models import Reviews
from reviews.serializers import ReviewSerializer


class ReviewViewSet(GenericViewSet):
    serializer_class = ReviewSerializer
    queryset = Reviews.objects.all()

    def list(self, request):
        PUBLISHED = 'published'
        queryset = Reviews.objects.select_related('author').filter(status=PUBLISHED)
        objects = self.paginate_queryset(queryset)
        serializer = ReviewSerializer(objects, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        if request.user.is_authenticated:
            serializer = ReviewSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get_permissions(self):
        permissions = []
        if self.action in ('create',):
            permissions.append(IsAuthenticated)
        return [permission() for permission in permissions]
