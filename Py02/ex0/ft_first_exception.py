def check_temperature(temp_str: str) -> (int | None):
    """
    A fun that filter out bad data before it corrupts the
    agricultural analytics

    :param temp_str: Description
    :type temp_str: str
    :return: Description
    :rtype: int | None
    """
    try:
        temp = int(temp_str)
    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number")
        return None

    if temp < 0:
        print(f"Error: {temp}°C is too cold for plants (min 0°C)")
        return None
    if temp > 40:
        print(f"Error: {temp}°C is too hot for plants (max 40°C)")
        return None
    else:
        print(f"Temperature {temp}°C is perfect for plants!")
        return temp


if __name__ == "__main__":
    def test_temperature_input() -> None:
        print("=== Garden Temperature Checker ===")

    test_values: list[str] = ["25", "abc", "100", "-50"]

    for value in test_values:
        print(f"Testing temperature: {value}")
        check_temperature(value)

    print("All tests completed - program didn't crash!")

    test_temperature_input()
