
# Egyptian tourism data and tools
EGYPTIAN_ATTRACTIONS = {
    "giza": {
        "name": "Pyramids of Giza",
        "location": "Giza Governorate",
        "ticket_price": "$15 for adults, $8 for students",
        "best_time": "Early morning (6-9 AM) or late afternoon (4-6 PM)",
        "description": "The Great Pyramid of Giza is the only surviving Wonder of the Ancient World."
    },
    "luxor": {
        "name": "Valley of the Kings",
        "location": "Luxor, Upper Egypt",
        "ticket_price": "$12 general entrance + $17 per tomb",
        "best_time": "October to April, early morning visits",
        "description": "Royal burial ground with 63 discovered tombs including Tutankhamun's."
    },
    "alexandria": {
        "name": "Bibliotheca Alexandrina",
        "location": "Alexandria",
        "ticket_price": "$3 for Egyptians, $9 for foreigners",
        "best_time": "Year-round, weekday mornings",
        "description": "Modern revival of the ancient Library of Alexandria."
    },
    "aswan": {
        "name": "Abu Simbel Temples",
        "location": "Aswan Governorate",
        "ticket_price": "$22 for adults",
        "best_time": "October to February, sunrise visits",
        "description": "Magnificent temples built by Ramesses II, relocated to save from flooding."
    },
    "cairo": {
        "name": "Khan el-Khalili Bazaar",
        "location": "Islamic Cairo",
        "ticket_price": "Free entry",
        "best_time": "Evening hours, avoid Friday afternoons",
        "description": "Historic marketplace dating back to the 14th century."
    }
}




def get_attraction_info(attraction_name: str) -> str:
    """Get information about Egyptian tourist attractions."""
    print(f"Tool get_attraction_info called for {attraction_name}")
    attraction_key = attraction_name.lower().replace(" ", "_").replace("'", "")
    
    # Try direct match first
    if attraction_key in EGYPTIAN_ATTRACTIONS:
        info = EGYPTIAN_ATTRACTIONS[attraction_key]
        return f"""
**{info['name']}**
📍 Location: {info['location']}
🎫 Ticket Price: {info['ticket_price']}
⏰ Best Time to Visit: {info['best_time']}
ℹ️ Description: {info['description']}
"""
    
    # Try partial matching
    for key, info in EGYPTIAN_ATTRACTIONS.items():
        if attraction_name.lower() in info['name'].lower() or key in attraction_name.lower():
            return f"""
**{info['name']}**
📍 Location: {info['location']}
🎫 Ticket Price: {info['ticket_price']}
⏰ Best Time to Visit: {info['best_time']}
ℹ️ Description: {info['description']}
"""
    
    return f"I don't have specific information about '{attraction_name}'. Try asking about: Pyramids of Giza, Valley of the Kings, Bibliotheca Alexandrina, Abu Simbel, or Khan el-Khalili."