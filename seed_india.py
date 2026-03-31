import os
import django
import random

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from destinations.models import Destination, LocalGuide, Homestay

def seed_data():
    print("🚀 Initializing Bharat AI Global Data Seed...")
    
    states_data = {
        "Andhra Pradesh": ["Araku Valley", "Tirupati", "Vizag Caves"],
        "Arunachal Pradesh": ["Tawang Monastery", "Ziro Valley"],
        "Assam": ["Kaziranga National Park", "Majuli Island"],
        "Bihar": ["Bodh Gaya", "Nalanda Ruins"],
        "Goa": ["Calangute Beach", "Dudhsagar Falls"],
        "Gujarat": ["Statue of Unity", "Rann of Kutch", "Gir Forest"],
        "Jharkhand": ["Hundru Falls", "Deoghar", "Netarhat"],
        "Karnataka": ["Hampi", "Coorg", "Mysore Palace"],
        "Kerala": ["Munnar", "Alleppey Backwaters"],
        "Rajasthan": ["Amer Fort", "Udaipur Lakes", "Jaisalmer Desert"],
        "Tamil Nadu": ["Madurai Meenakshi Temple", "Ooty", "Mahabalipuram"],
        "Uttar Pradesh": ["Taj Mahal", "Varanasi Ghats", "Lucknow Imambara"],
        # ... Add more states as needed
    }

    categories = ['ECO', 'CULTURAL']
    
    # We will generate 1000 items by looping and varying the descriptions
    for i in range(1, 1001):
        state = random.choice(list(states_data.keys()))
        base_name = random.choice(states_data[state])
        name = f"{base_name} Site-{i}"
        
        # 1. Create Destination
        dest = Destination.objects.create(
            name=name,
            state=state,
            category=random.choice(categories),
            description=f"Explore the majestic beauty of {name} in {state}. A hub of historical significance and breathtaking views.",
            visiting_time="9:00 AM - 6:00 PM",
        )

        # 2. Create 2-3 Verified Guides for this place
        for g in range(random.randint(2, 3)):
            LocalGuide.objects.create(
                destination=dest,
                name=f"Guide {dest.name} - {g+1}",
                phone=f"+91 {random.randint(600, 999)}{random.randint(1000000, 9999999)}",
                is_verified=True
            )

        # 3. Create 1-2 Verified Homestays for this place
        for h in range(random.randint(1, 2)):
            Homestay.objects.create(
                destination=dest,
                name=f"{dest.name} Residency {h+1}",
                contact=f"+91 {random.randint(700, 999)}1234567",
                amenities="WiFi, Breakfast, AC, Hot Water",
                price_per_night=random.randint(1500, 8000),
                is_verified=True
            )

        if i % 100 == 0:
            print(f"✅ {i} locations deployed...")

    print("✨ SUCCESS: 1,000 Indian Locations with Guides and Homestays are now LIVE.")

if __name__ == "__main__":
    seed_data()