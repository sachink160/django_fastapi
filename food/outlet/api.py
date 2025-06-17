from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from food.utils.permissions import IsAPIKEYAuthenticated
from food.outlet.models import *
from food.outlet.serializers import *

class RestorentViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    serializer_class = RestaurantSerializer

class FoodCategoryViewSet(viewsets.ModelViewSet):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]

class CuisineViewSet(viewsets.ModelViewSet):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]


class OutletViewSet(viewsets.ModelViewSet):
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    

class OutletStaffViewSet(viewsets.ModelViewSet):
    queryset = OutletStaff.objects.all()
    serializer_class = OutletStaffSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]


class MenuSectionViewSet(viewsets.ModelViewSet):
    queryset = MenuSection.objects.all()
    serializer_class = MenuSectionSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]

class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]


class FoodVariantViewSet(viewsets.ModelViewSet):
    queryset = FoodVariant.objects.all()
    serializer_class = FoodVariantSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]


class AddOnViewSet(viewsets.ModelViewSet):
    queryset = AddOn.objects.all()
    serializer_class = AddOnSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]


class SearchLogViewSet(viewsets.ModelViewSet):
    queryset = SearchLog.objects.all()
    serializer_class = SearchLogSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]