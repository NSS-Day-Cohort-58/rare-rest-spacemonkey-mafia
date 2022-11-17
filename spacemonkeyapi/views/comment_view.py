from rest_framework.decorators import action
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from spacemonkeyapi.models import Comment, Post, RareUser

class CommentView(ViewSet):
    def create(self, request, pk):
        """Handle POST operations

        Returns
            Response -- JSON serialized post instance
        """
        post = Post.objects.get(pk=pk)
        author = RareUser.objects.get(user=request.auth.user)
        comment = Comment.objects.create(
            post=post,
            author=author,
            content=request.data["content"],
            created_on=request.data["created_on"]
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        """Delete request for a user to delete a comment on a post"""
        author = RareUser.objects.get(user=request.auth.user)
        comment = Comment.objects.get(pk=pk, author=author)
        comment.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests to songs resource

        Returns:
            Response -- JSON serialized list of all comments for a post
        """
        #view for comments on a post
        post = Post.objects.get(pk=request.query_params.get('pk', None))
        comments = Comment.objects.all().filter(post=post)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag

        Returns:
            Response -- JSON serialized tag instance
        """
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    
    
    def update(self, request, pk=None):
        """Handle PUT requests for a tag

        Returns:
            Response -- Empty body with 204 status code
        """
        author = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["post"])
        comment = Comment.objects.get(pk=pk, author=author, post=post)
        comment.content = request.data["content"]
        comment.created_on = request.data["created_on"]
        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for tags

    Arguments:
        serializers
    """
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_on')
        depth = 1
