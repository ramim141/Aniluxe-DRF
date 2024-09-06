from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *

# List all categories
@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

# List products with filtering and sorting
@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()

    # Filtering by category
    category = request.query_params.get('category')
    if category:
        products = products.filter(category__name=category)
    
    # Filtering by color
    color = request.query_params.get('color')
    if color:
        products = products.filter(colors__contains=color)  # Changed from icontains to contains

    # Sorting by price, popularity, and rating
    sort_by = request.query_params.get('sort_by')
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'popularity':
        products = products.order_by('-rating')
    elif sort_by == 'rating':
        products = products.order_by('-rating')

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Get a specific product
@api_view(['GET'])
def get_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

# Add or update cart item
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    data = request.data
    user = request.user
    try:
        product = Product.objects.get(id=data['product_id'])
    except Product.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product,
        size=data['size'],
        color=data['color'],
        defaults={'quantity': data.get('quantity', 1)}
    )
    
    if not created:
        cart_item.quantity += data.get('quantity', 1)
        cart_item.save()

    serializer = CartSerializer(cart_item, many=False)
    return Response(serializer.data)

# Add item to wishlist
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    data = request.data
    user = request.user
    try:
        product = Product.objects.get(id=data['product_id'])
    except Product.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)
    serializer = WishlistSerializer(wishlist_item, many=False)
    return Response(serializer.data)

# Place an order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    data = request.data
    user = request.user
    try:
        product = Product.objects.get(id=data['product_id'])
    except Product.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.create(
        user=user,
        product=product,
        address=data['address'],
        quantity=data['quantity']
    )
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)

# Add a review
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    data = request.data
    user = request.user

    try:
        product = Product.objects.get(id=data['product_id'])
    except Product.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user has already reviewed the product
    # review_exists = Review.objects.filter(user=user, product=product).exists()
    review_exists = product.review_set.filter(user=user).exists()

    if review_exists:
        content = {'detail': 'Product already reviewed'}
        # return Response({"detail": "You have already reviewed this product."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif data['rating'] == 0:
        content = {'detail': 'Please Select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:

    # Create the new review
        review = Review.objects.create(
            user=user,
            product=product,
            # rating=data.get('rating', 0),
            rating=data['rating'],
            # comment=data.get('comment', '')
            comment=data['comment'],
        )
        
        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0

        for i in reviews:
            total += i.rating
        product.rating = total / len(reviews)
        product.save()
        return Response('Review Added')
    
        # Recalculate the product's average rating and total reviews count
        # reviews = product.reviews.all()
        # product.numReviews = reviews.count()
        # product.rating = reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
        # product.save()

        # serializer = ReviewSerializer(review, many=False)
        # return Response(serializer.data)


# Get cart items for the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)

# Get wishlist items for the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    serializer = WishlistSerializer(wishlist_items, many=True)
    return Response(serializer.data)

# Get orders for the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
