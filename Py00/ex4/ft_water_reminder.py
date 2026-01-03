
def ft_water_reminder():
    reminder = int(input("Days since last watering: "))
    if reminder > 2:
        print("Water the plants!")
    else:
        print("Plants are fine")
