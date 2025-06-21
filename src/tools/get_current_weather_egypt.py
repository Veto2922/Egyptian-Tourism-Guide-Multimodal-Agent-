def get_current_weather_egypt() -> str:
    """Get current weather information for major Egyptian cities."""
    print("Tool get_current_weather_egypt called")
    # This is a mock function - in real implementation, you'd call a weather API
    current_month = datetime.now().month
    
    if 5 <= current_month <= 9:  # Summer
        return """
🌡️ **Current Weather in Egypt (Summer):**
• Cairo: Very hot (35-40°C), low humidity
• Alexandria: Hot but more humid (30-35°C)
• Luxor/Aswan: Extremely hot (40-45°C)
• Red Sea Coast: Hot but pleasant sea breeze (32-38°C)

💡 **Travel Tips:** Stay hydrated, avoid midday sun, wear light colors and sun protection.
"""
    else:  # Winter/Spring/Fall
        return """
🌡️ **Current Weather in Egypt (Cooler Season):**
• Cairo: Pleasant (20-28°C), occasional rain
• Alexandria: Mild and humid (18-25°C)
• Luxor/Aswan: Warm and dry (25-32°C)
• Red Sea Coast: Perfect for diving (22-28°C)

💡 **Travel Tips:** Great weather for sightseeing! Bring light layers for evening.
"""