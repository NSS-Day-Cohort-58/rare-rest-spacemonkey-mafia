"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from spacemonkeyapi.models.user import User
from spacemonkeyapi.models.author import Author


class RareUserView(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for single post type

        Returns:
            Response -- JSON serialized post type
        """
        user_view = User.objects.get(pk=pk)
        serialized = RareUserSerializer(user_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all User
    def list(self, request):
        """Handle GET requests to get all post types

        Returns:
            Response -- JSON serialized list of post types
        """
        user_view = User.objects.all()
        serialized = RareUserSerializer(user_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model= Author
        fields = ('id', 'bio', 'age', 'profile_image', 'full_name')

class RareUserSerializer(serializers.ModelSerializer):

    author= AuthorSerializer(many=False)
    date_joined= serializers.DateTimeField(
        "%x"
    )

    class Meta:
        model = User
        fields = ('id','username','email', 'author', 'date_joined')