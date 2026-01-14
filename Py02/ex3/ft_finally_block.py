def water_plants(plant_list: list[str]) -> None:
    """
    A fun that:

    • Opens a "watering system" (just print a message)
    • Goes through each plant in the list
    • Waters each plant (print a message)
    • Always closes the watering system in a finally block
    • Handles errors if a plant name is invalid

    :param plant_list: Description
    :type plant_list: list[str]
    """

    print("Opening watering system")
    try:
        for plant_str in plant_list:
            plant_list = plant_str.capitalize()
            print(plant_list)
    except Exception:
        print("Error: Cannot water None - invalid plant!")
    finally:
        print("Closing watering system (cleanup)")


def test_watering_system() -> None:
    """
    A fun that demonstrates:

    • Watering with a bad plant list (causes an error)
    • Normal watering with a good plant list
    • Shows that cleanup always happens, even when there's an error
    • Uses try/except/finally structure
    """

    clean_list: list[str] = ["watering tomato", "watering lettuce",
                             "watering carrots"]
    risky_list: list[str] = ["watering tomato", None, "watering carrots"]
    print("Testing normal watering...")
    water_plants(clean_list)
    print("Watering completed successfully!\n")
    print("Testing with error...")
    water_plants(risky_list)


if __name__ == "__main__":
    print("=== Garden Watering System ===\n")
    test_watering_system()
    print()
    print("Cleanup always happens, even with errors!")
