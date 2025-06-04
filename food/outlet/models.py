import uuid
from django.db import models
from django.contrib.auth import get_user_model
# from food.custom_auth.models import BaseModel
# from django.contrib.postgres.fields import JSONField 
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from food.custom_auth.models import BaseModel


User = get_user_model()


class FoodCategory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name_plural = 'Food Categories'
    
    def __str__(self):
        return self.name

class Cuisine(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='cuisines/', blank=True, null=True)
    
    def __str__(self):
        return self.name

# Restaurant and Outlet Models
class Restaurant(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'producer'})
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='restaurants/logos/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='restaurants/banners/', blank=True, null=True)
    cuisines = models.ManyToManyField(Cuisine, blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=17)
    website = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Outlet(BaseModel):
    OUTLET_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('temporarily_closed', 'Temporarily Closed'),
        ('permanently_closed', 'Permanently Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='outlets')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               limit_choices_to={'user_type__in': ['outlet_manager', 'producer']})
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=17)
    email = models.EmailField(blank=True)
    
    # Operating hours
    monday_open = models.TimeField(null=True, blank=True)
    monday_close = models.TimeField(null=True, blank=True)
    tuesday_open = models.TimeField(null=True, blank=True)
    tuesday_close = models.TimeField(null=True, blank=True)
    wednesday_open = models.TimeField(null=True, blank=True)
    wednesday_close = models.TimeField(null=True, blank=True)
    thursday_open = models.TimeField(null=True, blank=True)
    thursday_close = models.TimeField(null=True, blank=True)
    friday_open = models.TimeField(null=True, blank=True)
    friday_close = models.TimeField(null=True, blank=True)
    saturday_open = models.TimeField(null=True, blank=True)
    saturday_close = models.TimeField(null=True, blank=True)
    sunday_open = models.TimeField(null=True, blank=True)
    sunday_close = models.TimeField(null=True, blank=True)
    
    delivery_available = models.BooleanField(default=True)
    pickup_available = models.BooleanField(default=True)
    dine_in_available = models.BooleanField(default=True)
    
    delivery_radius_km = models.PositiveIntegerField(default=5)
    minimum_order_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=OUTLET_STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    
    
    class Meta:
        unique_together = ['restaurant', 'name']
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"

# Staff Management
class OutletStaff(BaseModel):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('chef', 'Chef'),
        ('cashier', 'Cashier'),
        ('delivery', 'Delivery Person'),
        ('staff', 'General Staff'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name='staff')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = ['outlet', 'user']
    
    def __str__(self):
        return f"{self.user.full_name} - {self.outlet.name} ({self.role})"

# Menu and Food Items
class MenuSection(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name='menu_sections')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order', 'name']
        unique_together = ['outlet', 'name']
    
    def __str__(self):
        return f"{self.outlet.name} - {self.name}"

class FoodItem(BaseModel):
    FOOD_TYPE_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non_veg', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
        ('jain', 'Jain'),
    ]
    
    SPICE_LEVEL_CHOICES = [
        ('mild', 'Mild'),
        ('medium', 'Medium'),
        ('spicy', 'Spicy'),
        ('extra_spicy', 'Extra Spicy'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name='food_items')
    menu_section = models.ForeignKey(MenuSection, on_delete=models.CASCADE, related_name='items')
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True)
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    allergens = models.TextField(blank=True)
    
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES)
    spice_level = models.CharField(max_length=15, choices=SPICE_LEVEL_CHOICES, blank=True)
    
    preparation_time_minutes = models.PositiveIntegerField(default=15)
    calories = models.PositiveIntegerField(null=True, blank=True)
    
    image = models.ImageField(upload_to='food_items/', blank=True, null=True)
    
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    
    sort_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order', 'name']
        unique_together = ['outlet', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.outlet.name}"
    
    @property
    def final_price(self):
        return self.discounted_price if self.discounted_price else self.price

# Variants and Add-ons
class FoodVariant(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=50)  # e.g., "Small", "Medium", "Large"
    price_difference = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order']
        unique_together = ['food_item', 'name']
    
    def __str__(self):
        return f"{self.food_item.name} - {self.name}"

class AddOn(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name='addons')
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['outlet', 'name']
    
    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class FoodItemAddOn(BaseModel):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    addon = models.ForeignKey(AddOn, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['food_item', 'addon']

# Customer Reviews and Ratings
class Review(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'consumer'})
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    
    # Review categories
    food_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    service_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    delivery_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        target = self.food_item.name if self.food_item else self.outlet.name
        return f"{self.customer.full_name} - {target} ({self.rating}★)"

# Favorites
class Favorite(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'consumer'})
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
    
    class Meta:
        unique_together = [
            ['customer', 'outlet'],
            ['customer', 'food_item']
        ]
    
    def __str__(self):
        target = self.food_item.name if self.food_item else self.outlet.name
        return f"{self.customer.full_name} - {target}"

# Search and Analytics
class SearchLog(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    search_query = models.CharField(max_length=200)
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    results_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.search_query} - {self.created_at.date()}"
