
def validate_city(city):
    validated_cities = [
        {'Bucuresti': ['bucharest', 'bucuresti']},
        {'Cluj-Napoca': ['cluj napoca', 'cluj']}
    ]

    for item in validated_cities:
        for key, value in item.items():
            if city.lower() in value:
                return key
    return city



