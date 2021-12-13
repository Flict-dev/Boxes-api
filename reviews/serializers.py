from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from reviews.models import Reviews
from users.serializers import UserSerializer


class ReviewSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Reviews
        fields = (
            'id',
            'author',
            'status',
            'text',
            'created_at',
            'published_at',
        )

    def create(self, validated_data):
        request = self.context.get('request')
        review = Reviews(
            author=request.user,
            text=request.data['text'],
        )
        review.save()
        return review
