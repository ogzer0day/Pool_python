def check_invalid_values(plant_name, water_level, sunlight_hours) -> None:
    """
    A fun that raise invalide values.
    """

    if not plant_name or not plant_name.strip():
        raise ValueError("Plant name cannot be empty!\n")

    if water_level < 1:
        raise ValueError(
            f"Water level {water_level} is too low (min 1)\n"
        )
    if water_level > 10:
        raise ValueError(
            f"Water level {water_level} is too high (max 10)\n"
        )

    if sunlight_hours < 2:
        raise ValueError(
            f"Sunlight hours {sunlight_hours} is too low (min 2)\n"
        )
    if sunlight_hours > 12:
        raise ValueError(
            f"Sunlight hours {sunlight_hours} is too high (max 12)\n"
        )


def check_plant_health(plant_name, water_level, sunlight_hours) -> None:
    """
    A fun that:

    • Checks if the plant name is valid (not empty)
    • Checks if water level is reasonable (between 1 and 10)
    • Checks if sunlight hours are reasonable (between 2 and 12)
    • Raises appropriate errors with helpful messages when something is wrong
    • Returns a success message if everything is okay
    """

    check_invalid_values(plant_name, water_level, sunlight_hours)
    print(f"Plant '{plant_name}' is healthy!\n")


def test_plant_checks() -> None:
    """
    A function that demonstrates:

    • Testing with good values
    • Testing with bad plant name
    • Testing with bad water level
    • Testing with bad sunlight hours
    • Catching and handling each error appropriately
    """

    print("Testing good values...")
    check_plant_health("tomato", 10, 3)

    print("Testing empty plant name...")
    try:
        check_plant_health("", 10, 0)
    except ValueError as e:
        print("Error:", e)

    print("Testing bad water level...")
    try:
        check_plant_health("tomato", 15, 2)
    except ValueError as e:
        print("Error:", e)

    print("Testing bad sunlight hours...")
    try:
        check_plant_health("tomato", 10, 0)
    except ValueError as e:
        print("Error:", e)
    print()
    print("All error raising tests completed!")


if __name__ == "__main__":
    print("=== Garden Plant Health Checker ===\n")
    test_plant_checks()
