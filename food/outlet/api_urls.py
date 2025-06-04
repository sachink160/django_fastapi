from django.urls import include, path
from rest_framework.routers import SimpleRouter
from food.registrations import api

from food.outlet import api

router = SimpleRouter()

router.register("v1/restorent", api.RestorentViewSet, basename="restorent")
router.register("v1/foodcategory", api.FoodCategoryViewSet, basename="foodcategory")
router.register("v1/cuisine", api.CuisineViewSet, basename="cuisine")
router.register("v1/outlet", api.OutletViewSet, basename="outlet")
router.register("v1/outletstaff", api.OutletStaffViewSet, basename="outletstaff")
router.register("v1/menusection", api.MenuSectionViewSet, basename="menusection")
router.register("v1/fooditem", api.FoodItemViewSet, basename="fooditem")
router.register("v1/foodvariant", api.FoodVariantViewSet, basename="foodvariant")
router.register("v1/addon", api.AddOnViewSet, basename="addon")
router.register("v1/review", api.ReviewViewSet, basename="review")
router.register("v1/favorite", api.FavoriteViewSet, basename="favorite")
router.register("v1/searchlog", api.SearchLogViewSet, basename="searchlog")


app_name = "outlet"

urlpatterns = [
    path("", include(router.urls)),
]

