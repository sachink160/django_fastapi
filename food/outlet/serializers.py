from rest_framework import serializers
from food.outlet.models import *

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
                    "id", "owner", "name", "description", "logo", "banner_image", "cuisines",
                    "license_number", "contact_email", "contact_phone", "website", "is_active",
                    "is_verified", "update_time"
                )
        read_only_fields = ['id'] 

class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ['id', 'name', 'description', 'image', 'is_active', 'sort_order', 'create_time']


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['id', 'name', 'description', 'image', 'is_active', 'create_time']


class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outlet
        fields = [
                    'id',
                    'restaurant',
                    'manager',
                    'name',
                    'address',
                    'latitude',
                    'longitude',
                    'phone',
                    'email',
                    
                    # Operating hours
                    'monday_open', 'monday_close',
                    'tuesday_open', 'tuesday_close',
                    'wednesday_open', 'wednesday_close',
                    'thursday_open', 'thursday_close',
                    'friday_open', 'friday_close',
                    'saturday_open', 'saturday_close',
                    'sunday_open', 'sunday_close',

                    # Availability
                    'delivery_available',
                    'pickup_available',
                    'dine_in_available',

                    # Delivery settings
                    'delivery_radius_km',
                    'minimum_order_amount',
                    'delivery_fee',

                    # Status
                    'status',
                    'is_featured',
                    'average_rating',
                    'total_reviews',

                    # Inherited from BaseModel
                    'is_active',
                    'is_delete',
                    'create_time',
                    'update_time'
                ]

class OutletStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutletStaff
        fields = [
                    'id',
                    'outlet',
                    'user',
                    'role',
                    'hire_date',
                    'salary',
                    'is_active',
                    'is_delete',
                    'create_time',
                    'update_time'
                ]

class MenuSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuSection
        fields = [
            'id', 'outlet', 'name', 'description', 'sort_order',
            'is_active', 'is_delete', 'create_time', 'update_time'
        ]


class FoodItemSerializer(serializers.ModelSerializer):
    final_price = serializers.ReadOnlyField()

    class Meta:
        model = FoodItem
        fields = [
            'id', 'outlet', 'menu_section', 'category',
            'name', 'description', 'ingredients', 'allergens',
            'price', 'discounted_price', 'food_type', 'spice_level',
            'preparation_time_minutes', 'calories', 'image',
            'is_available', 'is_featured', 'is_bestseller',
            'average_rating', 'total_reviews', 'total_orders',
            'sort_order', 'final_price',
            'is_active', 'is_delete', 'create_time', 'update_time'
        ]


class FoodVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodVariant
        fields = [
            'id', 'food_item', 'name', 'price_difference',
            'is_available', 'sort_order',
            'is_active', 'is_delete', 'create_time', 'update_time'
        ]


class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOn
        fields = [
            'id', 'outlet', 'name', 'price', 'is_available',
            'is_active', 'is_delete', 'create_time', 'update_time'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id', 'customer', 'outlet', 'food_item',
            'rating', 'comment', 'food_rating',
            'service_rating', 'delivery_rating',
            'is_verified',
            'is_active', 'is_delete', 'create_time', 'update_time'
        ]

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = [
            'id',
            'customer',
            'outlet',
            'food_item',
        ]

class SearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchLog
        fields = [
            'id',
            'user',
            'search_query',
            'category',
            'location',
            'results_count',
            'create_time',
            'updated_time',
        ]