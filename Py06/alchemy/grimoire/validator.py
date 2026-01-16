
def validate_ingredients(ingredients: str) -> str:
    lis = ingredients.split(' ')
    check = [1 for val in lis if val in ["fire", "water", "earth", "air"]]
    if check:
        return (f"{ingredients} - VALID")
    else:
        return (f"{ingredients} - INVALID")
