from .elements import (create_fire, create_water,
                       create_air, create_earth)


def healing_potion() -> str:
    return (f"Healing potion brewed with {create_fire()} and"
            f"{create_water()}")


def strength_potion() -> str:
    return (f"Strength potion brewed with {create_earth()} and"
            f"{create_fire()}")


def invisibility_potion() -> str:
    return (f"Invisibility potion brewed with {create_air()} and"
            f"{create_water()}")


def wisdom_potion() -> str:
    return (f"Wisdom potion brewed with all elements: {list[create_fire(), create_water(), create_air(), create_earth()]}")
