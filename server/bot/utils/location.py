from bot.utils.cities import CITIES
# Поиск города для сохранения в normalize_location
async def normalize_city(city_name):
    print(f"Searching for city: {city_name}")
    for key, variants in CITIES.items():
        for variant in variants:
            if city_name.lower() in variant:
                print(f"Found city: {key}")
                return key
    return None