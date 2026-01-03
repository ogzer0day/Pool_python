def ft_count_harvest_recursive():
    def recursive_function(harvest):
        if harvest == 0:
            return 1
        else:
            recursive_function(harvest - 1)
            print(harvest)
    harvest = int(input("Days until harvest: "))
    recursive_function(harvest)
    print("Harvest time!")
