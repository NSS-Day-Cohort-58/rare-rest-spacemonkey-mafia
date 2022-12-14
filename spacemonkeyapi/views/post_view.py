from rest_framework.decorators import action
from django.http import HttpResponseServerError
from django.db.models import Case, When, Value, IntegerField, BooleanField
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from spacemonkeyapi.models import Post, RareUser, Tag, Comment, Category


class PostView(ViewSet):
    
    # View Single Post
    def retrieve(self, request, pk):
        """Handle GET requests for single post type

        Returns:
            Response -- JSON serialized post type
        """
        rare_user = RareUser.objects.get(user=request.auth.user)
        post_view = Post.objects.get(pk=pk)
        
        post_view.is_author = False

        if post_view.author == rare_user:
            post_view.is_author = True


        serialized = PostSerializer(post_view, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    # View all Post
    def list(self, request):
        """Handle GET requests to get all post types

        Returns:
            Response -- JSON serialized list of post types
        """
        rare_user = RareUser.objects.get(user=request.auth.user)

        post_view = Post.objects.annotate(
               is_author=Case(
                   When(author=rare_user,
                        then=Value(True)),
                   default=Value(False),
                   output_field=BooleanField())) \
                .all()

        if "category" in request.query_params:
            post_view = Post.objects.filter(category__id=request.query_params['category'])
        
        serialized = PostSerializer(post_view, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    # Create a Post
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized post instance
        """
        #~ these will need to be updated once the Authentication is Running.
        author = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])
        # tag = Tag.objects.get(pk=request.data["tag"])

        post = Post.objects.create(
            author=author,
            category=category,
            title=request.data["title"],
            publication_date=request.data["publication_date"],
            image_url=request.data["image_url"],
            content=request.data["content"],
            # tag=tag,
            approved=request.data["approved"],
        )
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # Edit Post (PUT)
    def update(self, request, pk):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """

        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        category = Category.objects.get(pk=request.data["category"])
        post.category = category
        
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)  


    # Delete Post
    def destroy(self, request, pk):
            post = Post.objects.get(pk=pk)
            post.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

    #create a posttag in the post view
    @action(methods=['post', 'delete'], detail=True)
    def posttag(self, request, pk=None):
        """Managing post tags"""
        post = Post.objects.get(pk=pk)
        if request.method == "POST":
            tag = Tag.objects.get(pk=request.data["tagId"])
            post.tags.add(tag)
            return Response({"Tag has been added"}, status=status.HTTP_204_NO_CONTENT)
        elif request.method == "DELETE":
            tag = Tag.objects.get(pk=request.data["tagId"])
            post.tags.remove(tag)
            return Response({"Tag has been removed"}, status=status.HTTP_204_NO_CONTENT)



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ('id', 'full_name', )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label', )


class PostSerializer(serializers.ModelSerializer):
    author= AuthorSerializer(many=False)
    category = CategorySerializer(many=False)
    class Meta:
        model = Post
        fields = ('id', 'author', 'is_author',
        'title', 'publication_date', 'image_url', 'content', 
        'approved', 'tags', 'comments', 'category',)
        depth = 1
