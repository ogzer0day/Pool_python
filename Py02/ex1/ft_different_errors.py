def ft_different_errors() -> None:
    """
    A fun that that demonstrates these common errors:

    • ValueError - when someone gives bad data (like "abc" instead of a number)
    • ZeroDivisionError - when you try to divide by zero
    • FileNotFoundError - when you try to open a file that doesn't exist
    • KeyError - when you look for something that isn't in a dictionary
    """
    try:
        int("sng")
    except ValueError:
        print("Testing ValueError...")
        print("Caught ValueError: invalid literal for int()")

    try:
        2 / 0
    except ZeroDivisionError:
        print("Testing ZeroDivisionError...")
        print("Caught ZeroDivisionError: division by zero")

    try:
        f = open("text.txt", '+r')
        f.read()
    except FileNotFoundError:
        print("Testing FileNotFoundError...")
        print("Caught FileNotFoundError: No such file 'missing.txt")

    try:
        dic = {"mohmed": 50, "zaka": 40}
        print(dic["hh"])
    except KeyError:
        print("Testing KeyError...")
        print("Caught KeyError: 'missing\\_plant'")

    try:
        int("abc") / 0
    except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError):
        print("Testing multiple errors together...")
        print("Caught an error, but program continues!")


def test_error_types() -> None:
    ft_different_errors()
    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
