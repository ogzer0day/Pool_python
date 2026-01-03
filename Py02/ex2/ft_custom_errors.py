class GardenError(Exception):
    """
    A basic error for garden problems.
    """
    pass


class PlantError(GardenError):
    """
    For problems with plants (inherits from GardenError).
    """
    pass


class WaterError(GardenError):
    """
    For problems with watering (inherits from GardenError).
    """
    pass


def check_WaterError() -> None:
    """
     A fun that raise a WaterError, that u can catch it later.
    """
    raise WaterError("Not enough water in the tank!")


def check_planerror() -> None:
    """
    A fun that raise a planerror, that u can catch it later.
    """
    raise PlantError("The tomato plant is wilting!")


try:
    print("Testing PlantError...")
    check_planerror()
except PlantError as e:
    print("Caught PlantError:", e)


try:
    print("Testing WaterError...")
    check_WaterError()
except WaterError as c:
    print("Caught WaterError:", c)


print("Testing catching all garden errors...")
for fun in (check_planerror, check_WaterError):
    try:
        fun()
    except GardenError as c:
        print("Caught a garden error:", c)
