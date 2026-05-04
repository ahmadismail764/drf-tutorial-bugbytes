from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, OrderItem, Product
from api.serializers import (
    OrderSerializer,
    ProductInfoSerializer,
    ProductSerializer,
    OrderCreateSerializer
)

# ==========================================
# PRODUCTS VIEWS
# ==========================================

# --- Function-Based Views ---

# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products': products,
#         'count': len(products),
#         'max_price': products.aggregate(max_price=Max('price'))['max_price']
#     })
#     return Response(serializer.data)

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all() # This is a queryset
#     # You pass this queryset into a serializer in order for
#     # the data to be serialized into sth accessible by the browser
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     # You pass this queryset into a serializer in order for
#     # the data to be serialized into sth accessible by the browser
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


# --- Class-Based Views ---

class ProductInfoAPIView(APIView):
    """
    A simple APIView to return aggregated information about products.
    It returns the total number of products and the maximum price across all products.
    """
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)

    # def delete(self, request):
    #     return Response({"message": "Method tested successfully"})


# --- Generic Views ---
# These are class-based views as well, but they have
# the most common operations encapsulated in generics such 
# they are easily inherited from and extended

"""
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreateAPIView(generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        print(request)
        return super().create(request, *args, **kwargs)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'
"""

class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    Handles listing all products (GET) and creating a new product (POST).
    Includes configured filtering (DjangoFilterBackend), searching (SearchFilter), 
    ordering (OrderingFilter), and a custom filter (InStockFilterBackend).
    """
    queryset = Product.objects.order_by('pk')
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
    ]
    search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = LimitOffsetPagination
    # pagination_class.page_size = 2
    # pagination_class.page_query_param = 'pagenum'
    # pagination_class.page_size_query_param = 'size' # type: ignore
    # pagination_class.max_page_size = 4

    def get_permissions(self):
        if self.request.method in ['GET', 'OPTIONS', 'HEAD']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a single Product instance based on product_id.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'


    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# --- ViewSets ---
# (None currently)


# ==========================================
# ORDERS VIEWS
# ==========================================

# --- Function-Based Views ---

# @api_view(['GET'])
# def order_list(request):
#     """
#     Retrieves a list of all orders, optionally prefetching related order items and products.
#     """
#     orders = Order.objects.prefetch_related('items__product')
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


# --- Class-Based Views ---
# (None currently)

# --- Generic Views ---

"""
class OrderListAPIView(generics.ListAPIView):
    # Retrieves a global list of all orders
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
    # Retrieves a list of orders specifically filtered for the currently authenticated user
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Override get_queryset to filter by the requesting user
        qs = super().get_queryset()
        filtered_orders = qs.filter(user=self.request.user)
        return filtered_orders
"""

# --- Viewsets ---

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    # @action(
    #         detail=False, 
    #         methods=['get'], 
    #         url_path='user-orders'
    # )
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)