#create class for tags
from rest_framework.decorators import action
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from spacemonkeyapi.models import Tag

class TagsView(ViewSet):
    def list(self, request):
        """Handle GET requests to songs resource

        Returns:
            Response -- JSON serialized list of songs
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag

        Returns:
            Response -- JSON serialized tag instance
        """
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized tag instance
        """
        tag = Tag.objects.create(
            name=request.data["name"]
        )
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a tag

        Returns:
            Response -- Empty body with 204 status code
        """
        tag = Tag.objects.get(pk=pk)
        tag.name = request.data["name"]
        tag.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single tag

        Returns:
            Response -- 200, 404, or 500 status code
        """
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags

    Arguments:
        serializers
    """
    class Meta:
        model = Tag
        fields = ('id', 'name')