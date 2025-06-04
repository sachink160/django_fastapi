from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from food.outlet.models import *
from food.outlet.serializers import *

class RestorentViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RestaurantSerializer

class FoodCategoryViewSet(viewsets.ModelViewSet):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    permission_classes = [IsAuthenticated]

class CuisineViewSet(viewsets.ModelViewSet):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer
    permission_classes = [IsAuthenticated]


class OutletViewSet(viewsets.ModelViewSet):
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer
    permission_classes = [IsAuthenticated]
    

class OutletStaffViewSet(viewsets.ModelViewSet):
    queryset = OutletStaff.objects.all()
    serializer_class = OutletStaffSerializer
    permission_classes = [IsAuthenticated]


class MenuSectionViewSet(viewsets.ModelViewSet):
    queryset = MenuSection.objects.all()
    serializer_class = MenuSectionSerializer
    permission_classes = [IsAuthenticated]


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]


class FoodVariantViewSet(viewsets.ModelViewSet):
    queryset = FoodVariant.objects.all()
    serializer_class = FoodVariantSerializer
    permission_classes = [IsAuthenticated]


class AddOnViewSet(viewsets.ModelViewSet):
    queryset = AddOn.objects.all()
    serializer_class = AddOnSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class SearchLogViewSet(viewsets.ModelViewSet):
    queryset = SearchLog.objects.all()
    serializer_class = SearchLogSerializer