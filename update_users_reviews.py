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

NAMES = ['Roja', 'Syed', 'Naveen', 'Kannan', 'Hari', 'Nitish', 'Nandhini', 'Wasim', 'Simron', 'Bala', 'Priya', 'Buela']

REVIEW_COMMENTS = [
    "Amazing product! Highly recommend. I saw drastic changes in just a few weeks.",
    "Very healthy plant, arrived in perfect condition. Packaging was incredibly secure.",
    "Would definitely buy again, my garden looks great.",
    "Good quality, solid packaging. Exactly what I needed.",
    "Breathtaking display and it grows so fast!",
    "Exactly as described. Impeccable root system. It is thriving on my windowsill.",
    "Beautiful foliage, really livens up my living room. Brings so much nature indoors.",
    "Customer service was great and the plant thrives. Five stars for the delivery process too.",
    "Just absolutely gorgeous! So much better than expected.",
    "A wonderful addition to my plant family! It's so cute.",
    "Unbelievable quality. I'll be recommending this nursery to all my friends.",
    "It requires minimal maintenance and handles low light perfectly.",
    "Vibrant colors! It bloomed beautifully right after potting."
]

try:
    with connection.cursor() as cursor:
        # 1. Delete ALL old reviews to wipe the slate clean
        cursor.execute("DELETE FROM reviews")
        
        # 2. Add new users
        users_to_add = []
        for name in NAMES:
            email = f"{name.replace(' ', '').lower()}@nurseryapp.com"
            # Using IGNORE allows this to run safely without failing on duplicates
            users_to_add.append((name, email, 'scrypt:32768:8:1$ZsPy9uzr$dummy', 'user'))
            
        cursor.executemany("INSERT IGNORE INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)", users_to_add)
        
        # 3. Retrieve their assigned IDs
        cursor.execute("SELECT id FROM users WHERE name IN %s", (tuple(NAMES),))
        user_ids = [r[0] for r in cursor.fetchall()]

        # 4. Fetch all available product IDs
        cursor.execute("SELECT id FROM products")
        product_ids = [r[0] for r in cursor.fetchall()]

        # 5. Insert new reviews for each product using strictly only the designated users
        all_reviews = []
        for pid in product_ids:
            num_reviews = random.randint(1, 4)
            # Make sure we don't pick more users than available
            sample_size = min(num_reviews, len(user_ids))
            selected_users = random.sample(user_ids, sample_size)
            for uid in selected_users:
                rating = random.randint(4, 5) 
                comment = random.choice(REVIEW_COMMENTS)
                all_reviews.append((uid, pid, rating, comment))
        
        cursor.executemany("INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (%s, %s, %s, %s)", all_reviews)
        
        connection.commit()
    print(f"Added {len(NAMES)} specific new users and flawlessly generated {len(all_reviews)} reviews.")
except Exception as e:
    print("Error:", e)
finally:
    connection.close()
