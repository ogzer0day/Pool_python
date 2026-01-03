class SecurePlant:
    """A simple program that get your plant secure"""
    def __init__(self, name, height, age):
        """
        Initialize a Plant object with a name, height, age, and trunk_diameter.
        """
        self.name = name
        self.__height = height
        self.__age = age

    def set_height(self, height):
        """
        A simple function that check height value is valid or not, if it valid
        we apdate the value, else we reject it.
        """
        if height < 0:
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
        else:
            self.__height = height
            print(f"Height updated: {self.__height}cm [OK]")

    def set_age(self, age):
        """
        A simple function that check age value is valid or not, if it valid
        we apdate the value, else we reject it.
        """
        if age < 0:
            print(f"Invalid operation attempted: age {age} days [REJECTED]")
            print("Security: Negative age rejected")
        else:
            self.__age = age
            print(f"Age updated: {self.__age} days [OK]")

    def get_height(self):
        """
        A simple function that return the valid height.
        """
        return self.__height

    def get_age(self):
        """
        A simple function that return the valid age.
        """
        return self.__age


if __name__ == "__main__":
    print("=== Garden Security System ===")
    plant = SecurePlant("Rose", 25, 30)
    print(f"Plant created: {plant.name}")

    plant.set_height(25)
    plant.set_age(30)
    print()
    plant.set_height(-5)
    print()
    print(
        f"Current plant: {plant.name} "
        f"({plant.get_height()}cm, {plant.get_age()} days)"
    )
