from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Avg
from .models import *

# Register your models here.
@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'sort_order', 'items_count', 'create_time')
    list_filter = ('is_active', 'create_time')
    search_fields = ('name', 'description')
    ordering = ('sort_order', 'name')
    list_editable = ('is_active', 'sort_order')
    
    def items_count(self, obj):
        count = obj.fooditem_set.count()
        if count > 0:
            url = reverse('admin:outlet_fooditem_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} items</a>', url, count)
        return '0 items'
    items_count.short_description = 'Food Items'

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'restaurants_count', 'create_time')
    list_filter = ('is_active', 'create_time')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    
    def restaurants_count(self, obj):
        count = obj.restaurant_set.count()
        if count > 0:
            url = reverse('admin:outlet_restaurant_changelist') + f'?cuisines__id__exact={obj.id}'
            return format_html('<a href="{}">{} restaurants</a>', url, count)
        return '0 restaurants'
    restaurants_count.short_description = 'Restaurants'

# Restaurant and Outlet Admin
class OutletInline(admin.TabularInline):
    model = Outlet
    extra = 0
    fields = ('name', 'address', 'phone', 'manager', 'status', 'is_featured')
    readonly_fields = ('create_time',)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'contact_phone', 'outlets_count', 'is_active', 'is_verified', 'create_time')
    list_filter = ('is_active', 'is_verified', 'cuisines', 'create_time')
    search_fields = ('name', 'owner__full_name', 'contact_phone', 'license_number')
    filter_horizontal = ('cuisines',)
    inlines = [OutletInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'name', 'description')
        }),
        ('Media', {
            'fields': ('logo', 'banner_image')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'website')
        }),
        ('Business Details', {
            'fields': ('license_number', 'cuisines')
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified')
        }),
    )
    
    readonly_fields = ('create_time', 'update_time')
    
    def outlets_count(self, obj):
        count = obj.outlets.count()
        active_count = obj.outlets.filter(status='active').count()
        if count > 0:
            url = reverse('admin:outlet_outlet_changelist') + f'?restaurant__id__exact={obj.id}'
            return format_html('<a href="{}">{} total ({} active)</a>', url, count, active_count)
        return '0 outlets'
    outlets_count.short_description = 'Outlets'

class OutletStaffInline(admin.TabularInline):
    model = OutletStaff
    extra = 0
    fields = ('user', 'role', 'is_active', 'hire_date')

class MenuSectionInline(admin.TabularInline):
    model = MenuSection
    extra = 0
    fields = ('name', 'is_active', 'sort_order')

@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'manager', 'phone', 'status', 'average_rating', 'delivery_available', 'create_time')
    list_filter = ('status', 'delivery_available', 'pickup_available', 'dine_in_available', 'is_featured', 'restaurant__name')
    search_fields = ('name', 'restaurant__name', 'phone', 'address')
    inlines = [OutletStaffInline, MenuSectionInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('restaurant', 'name', 'manager', 'address')
        }),
        ('Contact', {
            'fields': ('phone', 'email')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Operating Hours', {
            'fields': (
                ('monday_open', 'monday_close'),
                ('tuesday_open', 'tuesday_close'),
                ('wednesday_open', 'wednesday_close'),
                ('thursday_open', 'thursday_close'),
                ('friday_open', 'friday_close'),
                ('saturday_open', 'saturday_close'),
                ('sunday_open', 'sunday_close'),
            )
        }),
        ('Service Options', {
            'fields': ('delivery_available', 'pickup_available', 'dine_in_available')
        }),
        ('Delivery Settings', {
            'fields': ('delivery_radius_km', 'minimum_order_amount', 'delivery_fee')
        }),
        ('Status & Ratings', {
            'fields': ('status', 'is_featured', 'average_rating', 'total_reviews')
        }),
    )
    
    readonly_fields = ('average_rating', 'total_reviews', 'create_time', 'update_time')

@admin.register(OutletStaff)
class OutletStaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'outlet', 'role', 'is_active', 'hire_date', 'salary')
    list_filter = ('role', 'is_active', 'outlet__restaurant')
    search_fields = ('user__full_name', 'user__phone', 'outlet__name')
    date_hierarchy = 'hire_date'

# Menu Management Admin
class FoodItemInline(admin.TabularInline):
    model = FoodItem
    extra = 0
    fields = ('name', 'price', 'food_type', 'is_available', 'is_featured')
    readonly_fields = ('total_orders',)

@admin.register(MenuSection)
class MenuSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'outlet', 'is_active', 'sort_order', 'items_count', 'create_time')
    list_filter = ('is_active', 'outlet__restaurant')
    search_fields = ('name', 'outlet__name')
    list_editable = ('is_active', 'sort_order')
    inlines = [FoodItemInline]
    
    def items_count(self, obj):
        count = obj.items.count()
        available_count = obj.items.filter(is_available=True).count()
        if count > 0:
            url = reverse('admin:outlet_fooditem_changelist') + f'?menu_section__id__exact={obj.id}'
            return format_html('<a href="{}">{} total ({} available)</a>', url, count, available_count)
        return '0 items'
    items_count.short_description = 'Food Items'

class FoodVariantInline(admin.TabularInline):
    model = FoodVariant
    extra = 0
    fields = ('name', 'price_difference', 'is_available', 'sort_order')

class FoodItemAddOnInline(admin.TabularInline):
    model = FoodItemAddOn
    extra = 0
    fields = ('addon', 'is_required')

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'outlet', 'category', 'price', 'final_price', 'food_type', 'average_rating', 'total_orders', 'is_available', 'is_featured')
    list_filter = ('food_type', 'is_available', 'is_featured', 'is_bestseller', 'category', 'outlet__restaurant')
    search_fields = ('name', 'description', 'outlet__name')
    list_editable = ('is_available', 'is_featured')
    inlines = [FoodVariantInline, FoodItemAddOnInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('outlet', 'menu_section', 'category', 'name', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'discounted_price')
        }),
        ('Food Details', {
            'fields': ('food_type', 'spice_level', 'preparation_time_minutes', 'calories')
        }),
        ('Ingredients & Allergens', {
            'fields': ('ingredients', 'allergens')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status & Features', {
            'fields': ('is_available', 'is_featured', 'is_bestseller', 'sort_order')
        }),
        ('Statistics', {
            'fields': ('average_rating', 'total_reviews', 'total_orders')
        }),
    )
    
    readonly_fields = ('average_rating', 'total_reviews', 'total_orders', 'create_time', 'update_time')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('outlet', 'category', 'menu_section')

@admin.register(FoodVariant)
class FoodVariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_item', 'price_difference', 'is_available', 'sort_order')
    list_filter = ('is_available', 'food_item__outlet__restaurant')
    search_fields = ('name', 'food_item__name')
    list_editable = ('price_difference', 'is_available', 'sort_order')

@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'outlet', 'price', 'is_available', 'create_time')
    list_filter = ('is_available', 'outlet__restaurant')
    search_fields = ('name', 'outlet__name')
    list_editable = ('price', 'is_available')

# Reviews and Ratings Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'target_name', 'rating', 'food_rating', 'service_rating', 'is_verified', 'create_time')
    list_filter = ('rating', 'is_verified', 'create_time', 'outlet__restaurant')
    search_fields = ('customer__full_name', 'comment', 'outlet__name', 'food_item__name')
    readonly_fields = ('create_time',)
    
    def target_name(self, obj):
        if obj.food_item:
            return f"{obj.food_item.name} (Item)"
        elif obj.outlet:
            return f"{obj.outlet.name} (Outlet)"
        return "Unknown"
    target_name.short_description = 'Review Target'

# Customer Engagement Admin
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('customer', 'target_name', 'create_time')
    list_filter = ('create_time',)
    search_fields = ('customer__full_name', 'outlet__name', 'food_item__name')
    readonly_fields = ('create_time',)
    
    def target_name(self, obj):
        if obj.food_item:
            return f"{obj.food_item.name} (Item)"
        elif obj.outlet:
            return f"{obj.outlet.name} (Outlet)"
        return "Unknown"
    target_name.short_description = 'Favorite Item'

# Analytics Admin
@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('search_query', 'user', 'category', 'location', 'results_count', 'create_time')
    list_filter = ('category', 'create_time')
    search_fields = ('search_query', 'location', 'user__full_name')
    readonly_fields = ('create_time',)
    date_hierarchy = 'create_time'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'category')

# Custom Admin Site Configuration
admin.site.site_header = "Food Finder Admin Panel"
admin.site.site_title = "Food Finder Admin"
admin.site.index_title = "Welcome to Food Finder Administration"

# Custom Admin Actions
# def make_active(modeladmin, request, queryset):
#     queryset.update(is_active=True)
# make_active.short_description = "Mark selected items as active"

# def make_inactive(modeladmin, request, queryset):
#     queryset.update(is_active=False)
# make_inactive.short_description = "Mark selected items as inactive"

# def mark_verified(modeladmin, request, queryset):
#     queryset.update(is_verified=True)
# mark_verified.short_description = "Mark selected items as verified"

# # Add actions to relevant admin classes
# FoodCategoryAdmin.actions = [make_active, make_inactive]
# CuisineAdmin.actions = [make_active, make_inactive]
# RestaurantAdmin.actions = [make_active, make_inactive, mark_verified]