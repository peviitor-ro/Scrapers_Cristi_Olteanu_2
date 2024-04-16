
def validate_city(city):
    validated_cities = [
        {'Bucuresti': ['bucharest', 'bucuresti']},
        {'Cluj-Napoca': ['Cluj-Napoca', 'cluj']}
    ]
    try:
        item_city = city.lower()
    except:
        return None

    for item in validated_cities:
        for key, value in item.items():
            if item_city in value:
                return key
            else:
                return city


