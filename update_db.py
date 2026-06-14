# DB update script for fixing image names and adding dynamic reviews

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

IMAGE_MAPPING = {
    'Monstera Deliciosa': '/static/images/monstera_deliciosa.jpg',
    'Snake Plant (Sansevieria)': '/static/images/snake_plant.jpg',
    'Fiddle Leaf Fig': '/static/images/fiddle_leaf_fig.jpg',
    'Golden Pothos': '/static/images/golden_pothos.jpg',
    'Peace Lily': '/static/images/peace_lily.jpg',
    'Spider Plant': '/static/images/spider_plant.jpg',
    'ZZ Plant': '/static/images/zz_plant.jpg',
    'Calathea Ornata': '/static/images/calathea_plant.jpg',
    'Rubber Plant': '/static/images/rubber_plant.jpg',
    'Bird of Paradise': '/static/images/bird_of_paradise.jpg',
    'Boston Fern': '/static/images/boston_fern.jpg',
    'Aloe Vera': '/static/images/aloae_vera.jpg',
    'String of Pearls': '/static/images/string_of_pearls.jpg',
    'Jade Plant': '/static/images/jade.jpg',
    'Echeveria Elegans': '/static/images/echeveria_elegans.jpg',
    'Zebra Plant (Haworthia)': '/static/images/zebra_plants.jpg',
    "Burro's Tail": '/static/images/burros_tail.jpg',
    'Panda Plant': '/static/images/panda_plant.jpg',
    'Moonstones': '/static/images/moonstone.jpg',
    'Hens and Chicks': '/static/images/hens&chicks.jpg',
    'Gasteria': '/static/images/gasteria.jpg',
    'Bougainvillea (Pink)': '/static/images/bougainvillea.jpg',
    'Rosemary Bush': '/static/images/rosemary_bush.jpg',
    'Hibiscus (Red)': '/static/images/hibiscus.jpg',
    'Jasmine': '/static/images/jasmine.jpg',
    'Lavender': '/static/images/lavendar.jpg',
    'Hydrangea (Blue)': '/static/images/hydrangea.jpg',
    'Croton': '/static/images/croton.jpg',
    'Azalea': '/static/images/azalea.jpg',
    'Fuchsia': '/static/images/fuchsia.jpg',
    'Boxwood': '/static/images/boxwood.jpg',
    'Hostas': '/static/images/hostas.jpg',
    'Red Rose': '/static/images/red_rose.jpg',
    'Tulip': '/static/images/tulip.jpg',
    'Sunflower': '/static/images/sunflower.jpg',
    'Marigold': '/static/images/marigold.jpg',
    'Orchid (Phalaenopsis)': '/static/images/orchid.jpg',
    'Daisy': '/static/images/daisy.jpg',
    'Peony': '/static/images/peony.jpg',
    'Dahlia': '/static/images/peony.jpg',
    'Lily': '/static/images/lily.jpg',
    'Carnation': '/static/images/carnation.jpg',
    'Geranium': '/static/images/geranium.jpg',
    'Pansy': '/static/images/pansy.jpg',
    'Basil': '/static/images/basil.jpg',
    'Mint': '/static/images/mint.jpg',
    'Cilantro (Coriander)': '/static/images/cilantro.jpg',
    'Thyme': '/static/images/thyme.jpg',
    'Oregano': '/static/images/oregano.jpg',
    'Parsley': '/static/images/parsley.jpg',
    'Chives': '/static/images/chives.jpg',
    'Dill': '/static/images/dill.jpg',
    'Sage': '/static/images/sage.jpg',
    'Tarragon': '/static/images/tarragon.jpg',
    'Lemongrass': '/static/images/lemongrass.jpg',
    'Bonsai Tree': '/static/images/bonsai_tree.jpg',
    'Lemon Tree': '/static/images/lemon_tree.jpg',
    'Mango Tree (Alphonso)': '/static/images/mango.jpg',
    'Neem Tree': '/static/images/neem.jpg',
    'Guava Tree': '/static/images/guava.jpg',
    'Ficus Benjamina': '/static/images/ficus_benjamina.jpg',
    'Papaya Tree': '/static/images/papaya.jpg',
    'Apple Tree': '/static/images/apple.jpg',
    'Cherry Tree': '/static/images/cherry.jpg',
    'Olive Tree': '/static/images/olive.jpg',
    'Pine Tree': '/static/images/pine.jpg',
    'Maple Tree': '/static/images/maple.jpg',
    'Neem Oil Spray': '/static/images/neem_oil_spray.jpg',
    'Diatomaceous Earth': '/static/images/diatomaceous_earth.jpg',
    'Insecticidal Soap': '/static/images/insecticidal_soap.jpg',
    'Bacillus Thuringiensis (Bt)': '/static/images/bacillus_thurignisus.jpg',
    'Horticultural Oil': '/static/images/horticultural_oil.jpg',
    'Copper Fungicide': '/static/images/copper_fungicide.jpg',
    'Cherry Tomato Seeds': '/static/images/cherry_tomato_seeds.jpg',
    'Mixed Floral Seeds Packet': '/static/images/mixed_floral_pack.jpg',
    'Spinach Seeds': '/static/images/spinach_seeds.jpg',
    'Chili Pepper Seeds': '/static/images/chilli_pepper.jpg',
    'Microgreens Variety Pack': '/static/images/microgreen_variety_pack.jpg',
    'Pumpkin Seeds': '/static/images/pumpkin_seeds.jpg',
    'Terracotta Clay Pot (Medium)': '/static/images/teracotta_clay_pot.jpg',
    'Ceramic Glazed Planter': '/static/images/ceramic_glazed_planter.jpg',
    'Hanging Macrame Basket': '/static/images/hanging_macrame_basket.jpg',
    'Self-Watering Plastic Pot': '/static/images/self_watering_plastic_pot.jpg',
    'Wooden Barrel Planter': '/static/images/wooden_barrel_planter.jpg',
    'Galvanized Metal Tub': '/static/images/galvanized_metal_tub.jpg'
}

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
        # 1. Update Images
        for name, img_path in IMAGE_MAPPING.items():
            cursor.execute("UPDATE products SET image_url=%s WHERE name=%s", (img_path, name))
        
        # 2. Add Users for Reviews
        users_to_add = [
            ('Alice Green', 'alice@nursery.com', 'scrypt:32768:8:1$ZsPy9uzr$dummy'),
            ('Bob Planter', 'bob@nursery.com', 'scrypt:32768:8:1$ZsPy9uzr$dummy'),
            ('Carol Bloom', 'carol@nursery.com', 'scrypt:32768:8:1$ZsPy9uzr$dummy'),
            ('Dave Seeds', 'dave@nursery.com', 'scrypt:32768:8:1$ZsPy9uzr$dummy')
        ]
        cursor.executemany("INSERT IGNORE INTO users (name, email, password_hash) VALUES (%s, %s, %s)", users_to_add)
        
        # 3. Add Reviews
        cursor.execute("SELECT id FROM users WHERE email LIKE '%@nursery.com'")
        user_ids = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT id FROM products")
        product_ids = [r[0] for r in cursor.fetchall()]

        cursor.execute("DELETE FROM reviews WHERE user_id IN (%s, %s, %s, %s)" % tuple(user_ids[:4]))

        all_reviews = []
        for pid in product_ids:
            # max 4 reviews
            num_reviews = random.randint(1, 4)
            selected_users = random.sample(user_ids, num_reviews)
            for uid in selected_users:
                rating = random.randint(4, 5) 
                comment = random.choice(REVIEW_COMMENTS)
                all_reviews.append((uid, pid, rating, comment))
        
        cursor.executemany("INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (%s, %s, %s, %s)", all_reviews)
        
        connection.commit()
    print(f"Updated images and added {len(all_reviews)} reviews.")
except Exception as e:
    print("Error:", e)
finally:
    connection.close()
