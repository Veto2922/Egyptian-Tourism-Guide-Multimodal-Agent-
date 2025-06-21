TRANSPORTATION_INFO = {
    "cairo_metro": {
        "name": "Cairo Metro",
        "price": "7-20 EGP per ride",
        "routes": "3 main lines covering most of Cairo",
        "tips": "Women-only cars available, avoid rush hours"
    },
    "uber_careem": {
        "name": "Uber/Careem",
        "price": "20-50 EGP for short rides in Cairo",
        "availability": "Available in major cities",
        "tips": "Confirm pickup location, keep small bills"
    },
    "nile_cruise": {
        "name": "Nile River Cruise",
        "price": "$50-200 per day depending on luxury level",
        "routes": "Luxor to Aswan (3-7 days)",
        "tips": "Book in advance, October-April best weather"
    }
}


def get_transportation_info(transport_type: str = "") -> str:
    """Get transportation information for Egypt."""
    print(f"Tool get_transportation_info called for {transport_type}")
    
    if not transport_type:
        # Return general info
        transport_info = "🚌 **Transportation Options in Egypt:**\n\n"
        for key, info in TRANSPORTATION_INFO.items():
            transport_info += f"• **{info['name']}**: {info['price']} - {info['tips']}\n"
        return transport_info
    
    transport_key = transport_type.lower().replace(" ", "_")
    
    for key, info in TRANSPORTATION_INFO.items():
        if transport_key in key or transport_type.lower() in info['name'].lower():
            return f"""
🚌 **{info['name']}**
💰 Price: {info['price']}
ℹ️ Details: {info.get('routes', info.get('availability', 'Available'))}
💡 Tips: {info['tips']}
"""
    
    return "Available transportation: Cairo Metro, Uber/Careem, Nile River Cruises, buses, and taxis."
