from django.core.management.base import BaseCommand
from food.outlet.models import FoodCategory, Cuisine

class Command(BaseCommand):
    help = 'Create initial master data for food categories and cuisines'

    def handle(self, *args, **options):
        # Create Food Categories
        categories = [
            {'name': 'Appetizers', 'description': 'Starters and small plates'},
            {'name': 'Main Course', 'description': 'Primary dishes'},
            {'name': 'Desserts', 'description': 'Sweet treats and desserts'},
            {'name': 'Beverages', 'description': 'Drinks and beverages'},
            {'name': 'Snacks', 'description': 'Light snacks and finger foods'},
            {'name': 'Breakfast', 'description': 'Morning meals'},
            {'name': 'Lunch', 'description': 'Midday meals'},
            {'name': 'Dinner', 'description': 'Evening meals'},
            {'name': 'Street Food', 'description': 'Popular street foods'},
            {'name': 'Fast Food', 'description': 'Quick service foods'},
        ]
        
        for i, cat_data in enumerate(categories):
            category, created = FoodCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'sort_order': i * 10
                }
            )
            if created:
                self.stdout.write(f"Created category: {category.name}")
        
        # Create Cuisines
        cuisines = [
            {'name': 'North Indian', 'description': 'Traditional North Indian cuisine'},
            {'name': 'South Indian', 'description': 'Traditional South Indian cuisine'},
            {'name': 'Chinese', 'description': 'Chinese and Indo-Chinese dishes'},
            {'name': 'Italian', 'description': 'Italian cuisine including pizza and pasta'},
            {'name': 'Mexican', 'description': 'Mexican and Tex-Mex dishes'},
            {'name': 'Continental', 'description': 'European and Continental dishes'},
            {'name': 'Punjabi', 'description': 'Traditional Punjabi cuisine'},
            {'name': 'Gujarati', 'description': 'Traditional Gujarati cuisine'},
            {'name': 'Rajasthani', 'description': 'Traditional Rajasthani cuisine'},
            {'name': 'Bengali', 'description': 'Traditional Bengali cuisine'},
            {'name': 'Maharashtrian', 'description': 'Traditional Maharashtrian cuisine'},
            {'name': 'South Indian', 'description': 'Dosa, Idli, Vada, and other South Indian dishes'},
            {'name': 'Fast Food', 'description': 'Burgers, sandwiches, and quick bites'},
            {'name': 'Desserts', 'description': 'Sweet treats and traditional desserts'},
            {'name': 'Beverages', 'description': 'Traditional and modern drinks'},
        ]
        
        for cuisine_data in cuisines:
            cuisine, created = Cuisine.objects.get_or_create(
                name=cuisine_data['name'],
                defaults={'description': cuisine_data['description']}
            )
            if created:
                self.stdout.write(f"Created cuisine: {cuisine.name}")
        
        self.stdout.write(self.style.SUCCESS('Successfully created initial data!'))