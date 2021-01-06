from cargo import Item, Truck


def create_items_list_from_csv(file_name):
    items = []
    with open(file_name, "r") as csv:
        for line in csv.readlines():
            data = line.strip().split(";")
            name = data[-1]
            data = list(map(int, data[:-1]))
            i = Item(data[0], data[1], data[2], data[3], name)
            items.append(i)
    return items


def write_cargo_string_to_csv(file_name, cargo_string):
    with open(file_name, "w") as csv:
        csv.write(cargo_string)


def load_trucks(items_list, truck1, truck2):
    for item in items_list:
        while item.amount > 0:
            if not truck1.add_item(item):
                break
        while item.amount > 0:
            if not truck2.add_item(item):
                break
    total_value_on_trucks = truck1.get_value_on_truck() + truck2.get_value_on_truck()
    cargo_csv_string = truck1.get_cargo_csv_string() + truck2.get_cargo_csv_string()
    return (total_value_on_trucks, cargo_csv_string)


# sort items by value per gram (desc.)
items = create_items_list_from_csv("items_list.csv")
items.sort(key=lambda x: x.value_per_gram, reverse=True)

# create Trucks
t1 = Truck(1100000, 72400, items)
t2 = Truck(1100000, 85700, items)

result_a = load_trucks(items, t1, t2)

# switch loading order to find the best of both solutions
t1.driver_weight, t2.driver_weight = t2.driver_weight, t1.driver_weight

t1.clear_truck()
t2.clear_truck()

result_b = load_trucks(items, t1, t2)

if result_a[0] >= result_b[0]:
    write_cargo_string_to_csv("cargo_list.csv", f"Total-Value;{result_a[0]}\n{result_a[1]}")
else:
    write_cargo_string_to_csv("cargo_list.csv", f"Total-Value;{result_b[0]}\n{result_b[1]}")
