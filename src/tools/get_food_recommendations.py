
EGYPTIAN_CUISINE = {
    "koshari": {
        "name": "Koshari",
        "description": "Egypt's national dish with rice, pasta, lentils, and spicy tomato sauce",
        "price_range": "$2-5",
        "where_to_find": "Street vendors, Abou Tarek (famous chain)"
    },
    "ful_medames": {
        "name": "Ful Medames",
        "description": "Traditional breakfast of slow-cooked fava beans",
        "price_range": "$1-3",
        "where_to_find": "Local breakfast spots, street vendors"
    },
    "mahshi": {
        "name": "Mahshi",
        "description": "Stuffed vegetables with rice and herbs",
        "price_range": "$3-8",
        "where_to_find": "Traditional restaurants, home cooking"
    }
}


def get_food_recommendations(dish_name: str = "") -> str:
    """Get Egyptian food recommendations and information."""
    print(f"Tool get_food_recommendations called for {dish_name}")
    
    if not dish_name:
        # Return general recommendations
        recommendations = "🍽️ **Must-Try Egyptian Dishes:**\n\n"
        for key, info in EGYPTIAN_CUISINE.items():
            recommendations += f"• **{info['name']}**: {info['description']} ({info['price_range']})\n"
        return recommendations
    
    dish_key = dish_name.lower().replace(" ", "_")
    
    # Try direct or partial matching
    for key, info in EGYPTIAN_CUISINE.items():
        if dish_key in key or dish_name.lower() in info['name'].lower():
            return f"""
🍽️ **{info['name']}**
📝 Description: {info['description']}
💰 Price Range: {info['price_range']}
📍 Where to Find: {info['where_to_find']}
"""
    
    return f"I don't have specific information about '{dish_name}'. Popular Egyptian dishes include Koshari, Ful Medames, and Mahshi."
