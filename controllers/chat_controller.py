from utils.db import get_db_connection
import re

def process_chat_message(message):
    message = message.lower().strip()
    
    # 1. First, check for common greetings/support questions (from the old JS logic)
    if re.search(r'\b(hi|hello|hey|greetings)\b', message):
        return "Hello there! 🌿 How can I assist you with your plant journey today?"
    if re.search(r'\b(shipping|delivery|track)\b', message):
        return "We offer fast 3-day shipping! Orders over $50 usually ship free. You can track your order in the 'Orders' tab of your profile. 🚚"
    if re.search(r'\b(return|refund|policy)\b', message):
        return "If your plant arrives damaged, please take a photo within 48 hours and contact us for a full replacement! 📦"
    if re.search(r'\b(thank|thanks)\b', message):
        return "You're very welcome! Happy planting! 🌱"

    # 2. Extract potential keywords for database search.
    # Exclude common stop words roughly
    stop_words = {"i", "want", "some", "a", "an", "the", "do", "you", "have", "any", "look", "looking", "for", "is", "there", "show", "me", "what", "are", "can", "buy", "purchase"}
    words = re.findall(r'\b\w+\b', message)
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # We'll try to match products
            for kw in keywords:
                like_pattern = f"%{kw}%"
                cursor.execute("""
                    SELECT id, name, category, price 
                    FROM products 
                    WHERE name LIKE %s OR category LIKE %s OR description LIKE %s
                    ORDER BY 
                        CASE WHEN LOWER(name) = %s THEN 1
                             WHEN LOWER(name) LIKE %s THEN 2
                             WHEN LOWER(name) LIKE %s THEN 3
                             WHEN LOWER(name) LIKE %s THEN 4
                             ELSE 5
                        END
                    LIMIT 1
                """, (like_pattern, like_pattern, like_pattern, kw.lower(), f"{kw.lower()} %", f"% {kw.lower()} %", f"% {kw.lower()}"))
                
                product = cursor.fetchone()
                if product:
                    return f"I found something you might like! Check out the <a href='/product/{product['id']}' class='text-blue-700 underline font-semibold hover:text-blue-900'>{product['name']}</a> in our {product['category']} category for ₹{product['price']}."
                    
            # If no specific product matched, check for generic plant care questions
            if re.search(r'\b(indoor|inside|houseplant)\b', message):
                return "Indoor plants like Snake Plants, Monstera, or Pothos are perfect for purifying air! They generally require less direct sunlight. <a href='/products' class='text-blue-700 underline font-semibold hover:text-blue-900'>View our shop</a> to see current availability."
            if re.search(r'\b(outdoor|outside|garden)\b', message):
                return "For outdoors, consider looking at our flowering perennials or hardy succulents which can withstand weather changes."
            if re.search(r'\b(water|watering|drink)\b', message):
                return "Rule of thumb: Most plants only need water when the top 1-2 inches of soil feel dry. Overwatering is the #1 plant killer! 💧"
            if re.search(r'\b(light|sun|sunlight)\b', message):
                return "Different plants have different needs! 'Bright indirect light' means near a sunny window but not directly in the scorching sun rays. ☀️"
            if re.search(r'\b(yellow|brown|dying|sick|help)\b', message):
                return "Oh no! Yellow leaves usually mean overwatering or poor drainage. Brown crispy edges often mean underwatering or lack of humidity. Please check the soil!"
            return "I am a nursery assistant and can only answer questions related to plants, gardening, or our catalog. Please ask me about our <a href='/products' class='text-blue-700 underline font-semibold hover:text-blue-900'>Shop</a>!"
    except Exception as e:
        print("Error in chat controller:", e)
        return "I'm currently having a little trouble connecting to my plant database. Please try checking our Shop page directly!"
    finally:
        conn.close()
