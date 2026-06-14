import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    try:
        # First connect without DB to create the database if it doesn't exist
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        with connection.cursor() as cursor:
            # Read schema.sql
            with open('schema.sql', 'r') as file:
                sql_script = file.read()
            
            # Split commands by semicolon, ignoring empty ones
            sql_commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
            
            for cmd in sql_commands:
                try:
                    cursor.execute(cmd)
                except Exception as e:
                    print(f"Error executing command: {cmd[:50]}... => {e}")
            
            connection.commit()
            
            # Insert demo data for products
            cursor.execute("SELECT name FROM products")
            existing_names = {row[0] for row in cursor.fetchall()}
            
            products = [
                # Original & New Indoor
                ('Monstera Deliciosa', 'A classic indoor plant with beautiful split leaves.', 899.00, 'Indoor', 25, '/static/images/monstera_deliciosa.jpg'),
                ('Snake Plant (Sansevieria)', 'Requires very little care and survives in low light.', 450.00, 'Indoor', 50, '/static/images/snake_plant.jpg'),
                ('Fiddle Leaf Fig', 'A popular statement plant with large, glossy, violin-shaped leaves.', 1299.00, 'Indoor', 15, '/static/images/fiddle_leaf_fig.jpg'),
                ('Golden Pothos', 'The perfect plant for beginners with beautiful trailing vines.', 299.00, 'Indoor', 60, '/static/images/golden_pothos.jpg'),
                ('Peace Lily', 'Elegant white flowers and excellent air purifying qualities.', 550.00, 'Indoor', 40, '/static/images/peace_lily.jpg'),
                ('Spider Plant', 'Hardy indoor plant that produces cute baby plantlets.', 250.00, 'Indoor', 55, '/static/images/spider_plant.jpg'),
                ('ZZ Plant', 'Virtually indestructible with waxy, dark green leaves.', 799.00, 'Indoor', 35, '/static/images/zz_plant.jpg'),
                ('Calathea Ornata', 'Stunning pink striped leaves that move with the light.', 850.00, 'Indoor', 20, '/static/images/calathea_ornata.jpg'),
                ('Rubber Plant', 'Bold, dark dramatic foliage that grows into an indoor tree.', 699.00, 'Indoor', 30, '/static/images/rubber_plant.jpg'),
                ('Bird of Paradise', 'Large banana-like leaves for a tropical vibe.', 1500.0, 'Indoor', 15, '/static/images/bird_of_paradise.jpg'),
                ('Boston Fern', 'Classic houseplant with graceful, arching fronds.', 400.0, 'Indoor', 40, '/static/images/boston_fern.jpg'),

                # Original & New Succulents
                ('Aloe Vera', 'A handy succulent that helps soothe skin and purifies air.', 199.00, 'Succulents', 100, '/static/images/aloae_vera.jpg'),
                ('String of Pearls', 'A unique trailing succulent that resembles small green pearls.', 399.00, 'Succulents', 30, '/static/images/string_of_pearls.jpg'),
                ('Jade Plant', 'A popular symbol of good luck and prosperity.', 299.00, 'Succulents', 80, '/static/images/jade_plant.jpg'),
                ('Echeveria Elegans', 'Beautiful rosette shape with powdery blue-green leaves.', 150.00, 'Succulents', 150, '/static/images/echeveria.jpg'),
                ('Zebra Plant (Haworthia)', 'Small succulent with striking white zebra-like stripes.', 180.00, 'Succulents', 60, '/static/images/zebra_plant.jpg'),
                ('Burro''s Tail', 'Fleshy, trailing stems that look like a braided tail.', 350.00, 'Succulents', 40, '/static/images/burros_tail.jpg'),
                ('Panda Plant', 'Fuzzy leaves with brownish-red margins. Fun to touch!', 250.00, 'Succulents', 50, '/static/images/panda_plant.jpg'),
                ('Moonstones', 'Charming succulent with plump, pastel-colored leaves.', 250.0, 'Succulents', 70, '/static/images/moonstones.jpg'),
                ('Hens and Chicks', 'Cold-hardy rosettes that multiply quickly.', 180.0, 'Succulents', 100, '/static/images/hens_and_chicks.jpg'),
                ('Gasteria', 'Thick, textured leaves that tolerate low light well.', 220.0, 'Succulents', 80, '/static/images/gasteria.jpg'),

                # Original & New Outdoor
                ('Bougainvillea (Pink)', 'A vibrant outdoor climber that adds a pop of color to any garden.', 750.00, 'Outdoor', 20, '/static/images/bougainvillea.jpg'),
                ('Rosemary Bush', 'Fragrant herb that works beautifully in gardens and outdoors.', 349.00, 'Outdoor', 40, '/static/images/rosemary_bush.jpg'),
                ('Hibiscus (Red)', 'Large, showy flowers that attract butterflies and hummingbirds.', 450.00, 'Outdoor', 35, '/static/images/hibiscus.jpg'),
                ('Jasmine', 'Known for its incredibly fragrant, tiny white flowers.', 399.00, 'Outdoor', 50, '/static/images/jasmine.jpg'),
                ('Lavender', 'Aromatic foliage and beautiful purple blooms.', 350.00, 'Outdoor', 60, '/static/images/lavender.jpg'),
                ('Hydrangea (Blue)', 'Lush shrub with huge, magnificent flower heads.', 600.00, 'Outdoor', 25, '/static/images/hydrangea.jpg'),
                ('Croton', 'Bright, multi-colored foliage perfect for sunny yards.', 420.00, 'Outdoor', 45, '/static/images/croton.jpg'),
                ('Azalea', 'Beautiful flowering shrub perfect for part-shade borders.', 550.0, 'Outdoor', 30, '/static/images/azalea.jpg'),
                ('Fuchsia', 'Striking two-toned flowers, great for hanging baskets.', 350.0, 'Outdoor', 40, '/static/images/fuchsia.jpg'),
                ('Boxwood', 'Evergreen shrub, ideal for tight hedges and topiary.', 450.0, 'Outdoor', 60, '/static/images/boxwood.jpg'),
                ('Hostas', 'Lush foliage plants that thrive in shade gardens.', 300.0, 'Outdoor', 50, '/static/images/hostas.jpg'),

                # Original & New Flowers
                ('Red Rose', 'Classic beautiful red roses for your garden.', 199.00, 'Flowers', 100, '/static/images/red_rose.jpg'),
                ('Tulip', 'Colorful spring-blooming flower.', 150.00, 'Flowers', 50, '/static/images/tulip.jpg'),
                ('Sunflower', 'Bright, cheerful flowers that follow the sun.', 120.00, 'Flowers', 200, '/static/images/sunflower.jpg'),
                ('Marigold', 'Vibrant orange and yellow blooms, great for repelling pests.', 90.00, 'Flowers', 300, '/static/images/marigold.jpg'),
                ('Orchid (Phalaenopsis)', 'Elegant, long-lasting blooms for indoor beauty.', 899.00, 'Flowers', 20, '/static/images/orchid.jpg'),
                ('Daisy', 'Classic, innocent and happy white petaled flowers.', 110.00, 'Flowers', 150, '/static/images/daisy.jpg'),
                ('Peony', 'Large, incredibly fragrant and romantic blossoms.', 550.00, 'Flowers', 30, '/static/images/peony.jpg'),
                ('Dahlia', 'Spectacular, intricate blooms that bloom in late summer.', 450.0, 'Flowers', 40, '/static/images/dahlia.jpg'),
                ('Lily', 'Large, prominent flowers with a rich fragrance.', 350.0, 'Flowers', 60, '/static/images/lily.jpg'),
                ('Carnation', 'Long-lasting ruffled flowers in varied colors.', 150.0, 'Flowers', 120, '/static/images/carnation.jpg'),
                ('Geranium', 'Popular bedding plants with clusters of bright flowers.', 200.0, 'Flowers', 90, '/static/images/geranium.jpg'),
                ('Pansy', 'Cheerful flowers that look like smiling faces.', 100.0, 'Flowers', 150, '/static/images/pansy.jpg'),

                # Original & New Herbs
                ('Basil', 'A fragrant herb commonly used in cooking.', 99.00, 'Herbs', 200, '/static/images/basil.jpg'),
                ('Mint', 'Refreshing herb easy to grow indoors or outdoors.', 89.00, 'Herbs', 150, '/static/images/mint.jpg'),
                ('Cilantro (Coriander)', 'Essential herb for Mexican and Asian cuisines.', 80.00, 'Herbs', 180, '/static/images/cilantro.jpg'),
                ('Thyme', 'Drought-tolerant herb with tiny leaves and great flavor.', 110.00, 'Herbs', 120, '/static/images/thyme.jpg'),
                ('Oregano', 'A must-have hardy herb for Italian dishes.', 120.00, 'Herbs', 140, '/static/images/oregano.jpg'),
                ('Parsley', 'Versatile garnish and flavor enhancer, rich in vitamins.', 90.00, 'Herbs', 160, '/static/images/parsley.jpg'),
                ('Chives', 'Mild onion flavor, great for salads and baked potatoes.', 100.00, 'Herbs', 130, '/static/images/chives.jpg'),
                ('Dill', 'Tall, feathery herb great for pickling and seafood.', 80.0, 'Herbs', 200, '/static/images/dill.jpg'),
                ('Sage', 'Velvety grey-green leaves with a robust, earthy flavor.', 120.0, 'Herbs', 130, '/static/images/sage.jpg'),
                ('Tarragon', 'Aromatic herb with a subtle licorice flavor.', 130.0, 'Herbs', 100, '/static/images/tarragon.jpg'),
                ('Lemongrass', 'Tall, grass-like stems with a strong citrusy scent.', 160.0, 'Herbs', 90, '/static/images/lemongrass.jpg'),

                # Original & New Trees
                ('Bonsai Tree', 'A miniature tree perfect for indoor decoration.', 999.00, 'Trees', 10, '/static/images/bonsai_tree.jpg'),
                ('Lemon Tree', 'A beautiful citrus tree for your backyard.', 1500.00, 'Trees', 5, '/static/images/lemon_tree.jpg'),
                ('Mango Tree (Alphonso)', 'The king of fruits! Grafted plant for quick yielding.', 1200.00, 'Trees', 15, '/static/images/mango_tree.jpg'),
                ('Neem Tree', 'Fast-growing tree known for exceptional medicinal properties.', 400.00, 'Trees', 40, '/static/images/neem_tree.jpg'),
                ('Guava Tree', 'Hardy fruit tree that produces sweet, tropical fruits.', 600.00, 'Trees', 20, '/static/images/guava_tree.jpg'),
                ('Ficus Benjamina', 'Elegant weeping fig tree for indoor or protected outdoor areas.', 800.00, 'Trees', 25, '/static/images/ficus.jpg'),
                ('Papaya Tree', 'Fast growing tree yielding large delicious fruits.', 350.00, 'Trees', 35, '/static/images/papaya_tree.jpg'),
                ('Apple Tree', 'Grow your own crisp, sweet apples at home.', 1800.0, 'Trees', 10, '/static/images/apple_tree.jpg'),
                ('Cherry Tree', 'Spring blossoming tree yielding delicious cherries.', 2000.0, 'Trees', 8, '/static/images/cherry_tree.jpg'),
                ('Olive Tree', 'Mediterranean classic with beautiful silvery foliage.', 2500.0, 'Trees', 5, '/static/images/olive_tree.jpg'),
                ('Pine Tree', 'Evergreen classic, perfect for large landscapes.', 900.0, 'Trees', 20, '/static/images/pine_tree.jpg'),
                ('Maple Tree', 'Spectacular autumn colors for your yard.', 1600.0, 'Trees', 12, '/static/images/maple_tree.jpg'),

                # Organic Pesticides
                ('Neem Oil Spray', '100% cold-pressed neem oil to get rid of aphids and mites naturally.', 350.00, 'Organic Pesticides', 100, '/static/images/neem_oil.jpg'),
                ('Diatomaceous Earth', 'Natural powder that effectively controls crawling insects safely.', 250.00, 'Organic Pesticides', 80, '/static/images/diatomaceous_earth.jpg'),
                ('Insecticidal Soap', 'Gentle, natural soap mixture that tackles soft-bodied pests.', 200.00, 'Organic Pesticides', 120, '/static/images/insecticidal_soap.jpg'),
                ('Bacillus Thuringiensis (Bt)', 'Biological pesticide excellent for caterpillar control.', 450.00, 'Organic Pesticides', 50, '/static/images/bt_spray.jpg'),
                ('Horticultural Oil', 'Smothers over-wintering insects and their eggs on trees.', 300.00, 'Organic Pesticides', 60, '/static/images/horticultural_oil.jpg'),
                ('Copper Fungicide', 'Organic disease control for blight, mildew, and black spot.', 450.0, 'Organic Pesticides', 50, '/static/images/copper_fungicide.jpg'),

                # Seeds
                ('Cherry Tomato Seeds', 'Grow your own delicious and sweet bite-sized tomatoes.', 50.00, 'Seeds', 500, '/static/images/tomato_seeds.jpg'),
                ('Mixed Floral Seeds Packet', 'A delightful mix of easy-to-grow summer flowers.', 60.00, 'Seeds', 400, '/static/images/floral_mixed_seeds.jpg'),
                ('Spinach Seeds', 'Nutrient-packed leafy greens that grow quickly.', 45.00, 'Seeds', 300, '/static/images/spinach_seeds.jpg'),
                ('Chili Pepper Seeds', 'Spicy and vibrant peppers perfect for home gardens.', 55.00, 'Seeds', 250, '/static/images/chili_seeds.jpg'),
                ('Microgreens Variety Pack', 'Grow superfoods right on your kitchen counter in days.', 120.00, 'Seeds', 150, '/static/images/microgreens_seeds.jpg'),
                ('Pumpkin Seeds', 'Perfect for autumn harvest.', 70.0, 'Seeds', 200, '/static/images/pumpkin_seeds.jpg'),

                # Pots
                ('Terracotta Clay Pot (Medium)', 'Classic, breathable clay pot perfect for succulents and herbs.', 150.00, 'Pots', 200, '/static/images/terracotta_pot.jpg'),
                ('Ceramic Glazed Planter', 'Elegant white glazed planter for your premium indoor plants.', 450.00, 'Pots', 80, '/static/images/ceramic_pot.jpg'),
                ('Hanging Macrame Basket', 'Bohemian style hanging planter for trailing varieties.', 350.00, 'Pots', 100, '/static/images/macrame_planter.jpg'),
                ('Self-Watering Plastic Pot', 'Convenient planter with reservoir for busy plant parents.', 280.00, 'Pots', 150, '/static/images/self_watering_pot.jpg'),
                ('Wooden Barrel Planter', 'Rustic oak-style half barrel, perfect for small trees or shrubs.', 850.00, 'Pots', 30, '/static/images/barrel_planter.jpg'),
                ('Galvanized Metal Tub', 'Modern industrial style tub, perfect for outdoor statement plants.', 550.0, 'Pots', 40, '/static/images/metal_tub.jpg')
            ]
            
            # Filter to only insert what is missing
            new_products = [p for p in products if p[0] not in existing_names]
            
            if new_products:
                print(f"Inserting {len(new_products)} new products...")
                cursor.executemany(
                    "INSERT INTO products (name, description, price, category, stock, image_url) VALUES (%s, %s, %s, %s, %s, %s)",
                    new_products
                )
                connection.commit()
            else:
                print("No new products to insert.")
                
            print("Database initialized successfully!")
    except Exception as e:
        print(f"Failed to connect or initialize DB: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == '__main__':
    init_db()
