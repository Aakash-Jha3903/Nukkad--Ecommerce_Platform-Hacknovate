import os
import django
import random
from app.models import Slider

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce_project.settings')
django.setup()

# Function to generate random slider data
def generate_random_slider(image_folder):
    DISCOUNT_DEAL_CHOICES = ['HOT DEALS', 'New Arrivals']
    BRAND_NAMES = ['Brand A', 'Brand B', 'Brand C']
    DISCOUNT_RANGE = range(10, 50, 5)

    # Get list of image files in the specified folder
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    # Choose a random image file from the folder
    image_path = random.choice(image_files)

    return Slider.objects.create(
        Image=image_path,
        Discount_Deal=random.choice(DISCOUNT_DEAL_CHOICES),
        SALE=random.randint(50, 500),  # Example range for sale price
        Brand_Name=random.choice(BRAND_NAMES),
        Discount=random.choice(DISCOUNT_RANGE),
        Link='http://example.com'
    )

# Generate and save random slider data
def insert_random_data(num_instances, image_folder):
    for _ in range(num_instances):
        generate_random_slider(image_folder)

if __name__ == '__main__':
    # Change the number to specify how many instances you want to create
    insert_random_data(1, '/path/to/your/image/folder')  # Example: Create 10 random instances from the specified folder
