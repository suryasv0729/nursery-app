import pymysql
import os
import random
from dotenv import load_dotenv

load_dotenv()

connection = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database='nursery_db'
)

def get_random_data(category):
    origins = {
        'Indoor': ['Tropical Rainforests of South America', 'Southeast Asia', 'Central American Jungles', 'South Africa'],
        'Outdoor': ['Mediterranean Region', 'North America', 'European Highlands', 'East Asian Forests'],
        'Succulents': ['Arid regions of Mexico', 'South African Deserts', 'Madagascar', 'Southwestern United States'],
        'Flowers': ['Himalayan foothills', 'Dutch cultivated fields', 'Asian Tropics', 'European Meadows'],
        'Herbs': ['Mediterranean Basin', 'Middle East', 'Southern Europe', 'North Africa'],
        'Trees': ['North American Forests', 'Amazon Basin', 'East Asia', 'Northern Europe'],
        'default': ['Global cultivated origins', 'Unknown wild origin', 'Hybrid origin']
    }
    
    bloom_times = {
        'Indoor': ['Rarely blooms indoors', 'Intermittent throughout the year', 'Late Spring to Summer'],
        'Outdoor': ['Early Spring', 'Late Summer to Fall', 'Continuous through Summer'],
        'Succulents': ['Late Winter to Spring', 'Summer blooms under full sun', 'Rarely blooms'],
        'Flowers': ['Spring to Summer', 'Continuous blooming season', 'Late Summer'],
        'Herbs': ['Mid-Summer', 'Spring', 'Late Summer to Early Autumn'],
        'Trees': ['Early Spring before leaves', 'Late Spring depending on species', 'Summer'],
        'default': ['Spring', 'Summer', 'Varies globally']
    }
    
    medicinal = [
        "Known for its air-purifying qualities, aiding respiratory health.",
        "Traditional medicine uses extracts to treat skin conditions.",
        "Contains mild natural compounds used to reduce inflammation.",
        "Often brewed in teas to calm the stomach and reduce nausea.",
        "Aromatherapy benefits include alleviating mild headaches.",
        "Historically used to promote better sleep when placed near the bed.",
        "No major medicinal uses, purely ornamental."
    ]
    
    other_uses = [
        "Excellent focal piece for interior minimalist design.",
        "Often used as a companion plant to deter certain pests.",
        "Provides excellent shade and wind barrier in outdoor gardens.",
        "Can be used for natural dyeing of fabrics.",
        "Popular gift plant indicating prosperity and good luck.",
        "Attracts friendly pollinators like bees and butterflies.",
        "Aesthetically pleasing for landscaping borders."
    ]
    
    psychology_notes = [
        "Reduces stress levels and promotes a sense of calm.",
        "Increases productivity and focus in workspace environments.",
        "The vibrant colors naturally boost serotonin and elevate mood.",
        "Caring for this plant instills a sense of routine and mindfulness.",
        "Known to lower blood pressure just by being in physical proximity.",
        "Enhances psychological well-being through biophilic connection.",
        "Inspires creativity and brightens up gloomy spaces."
    ]
    
    watering = [
        "Every 3-4 days; keep soil slightly moist.",
        "Once a week; allow topsoil to dry completely.",
        "Every 2 weeks; highly drought tolerant.",
        "Daily misting or watering required during summer.",
        "Only when the top 2 inches of soil feel bone dry.",
        "Moderate watering, twice a week.",
        "Likes to stay moist but not waterlogged."
    ]
    
    cat = category if category in origins else 'default'
    
    return {
        'origin': random.choice(origins[cat]),
        'bloom_time': random.choice(bloom_times[cat]),
        'medicinal_uses': random.choice(medicinal),
        'other_uses': random.choice(other_uses),
        'psychology_note': random.choice(psychology_notes),
        'watering_time': random.choice(watering)
    }

try:
    with connection.cursor() as cursor:
        # Alter table
        print("Modifying database schema...")
        columns_to_add = [
            ("origin", "VARCHAR(255)"),
            ("bloom_time", "VARCHAR(255)"),
            ("medicinal_uses", "TEXT"),
            ("other_uses", "TEXT"),
            ("psychology_note", "TEXT"),
            ("watering_time", "VARCHAR(255)")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE products ADD COLUMN {col_name} {col_type};")
            except pymysql.err.OperationalError as e:
                # 1060 is Duplicate column name
                if e.args[0] == 1060:
                    pass
                else:
                    raise e
                    
        # Seed Data
        print("Seeding botanical data to existing products...")
        cursor.execute("SELECT id, category FROM products")
        products = cursor.fetchall()
        
        for pid, cat in products:
            data = get_random_data(cat)
            cursor.execute('''
                UPDATE products 
                SET origin=%s, bloom_time=%s, medicinal_uses=%s, other_uses=%s, psychology_note=%s, watering_time=%s
                WHERE id=%s
            ''', (data['origin'], data['bloom_time'], data['medicinal_uses'], data['other_uses'], data['psychology_note'], data['watering_time'], pid))
            
        connection.commit()
    print("Successfully added columns and seeded botanical data for", len(products), "products.")
except Exception as e:
    print("Error:", e)
finally:
    connection.close()
