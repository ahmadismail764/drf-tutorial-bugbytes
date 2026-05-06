from django.db import transaction
from rest_framework import serializers
from orders.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price',
    )

    class Meta:
        model = OrderItem
        fields = ('product_name', 'product_price', 'quantity', 'item_subtotal')

class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return sum(item.item_subtotal for item in obj.items.all())

    class Meta:
        model = Order
        fields = ('order_id', 'created_at', 'user', 'status', 'items', 'total_price')
        extra_kwargs = {
            'user': {'read_only': True}
        }

class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)


    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in orderitem_data:
                OrderItem.objects.create(order=order, **item)

        return order
    
    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop('items', None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if orderitem_data:
                # clear existing items (optional, depedns on requirements of course)
                instance.items.all().delete()

                # then recreate the new ones
                for item in orderitem_data:
                    OrderItem.objects.create(order=instance, **item)
        return instance



    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items'
        )
        extra_kwargs = {
            'user': {'read_only': True}
        }