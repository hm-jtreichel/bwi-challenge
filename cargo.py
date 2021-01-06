class Item:

    def __init__(self, id, amount, weight, value, name="N/A"):
        self.id = id
        self.amount = amount
        self.weight = weight
        self.value = value
        self.name = name
        self.value_per_gram = value / weight


class Truck:

    def __init__(self, max_weight, driver_weight, items_list):
        self.max_weight = max_weight
        self.driver_weight = driver_weight
        self.current_weight = driver_weight
        self.items_on_truck = {}
        self.items_list = items_list


    # adds one of an item to truck (if there still is one in warehouse)
    def add_item(self, item):
        if self.current_weight + item.weight > self.max_weight:
            return False
        self.items_on_truck[item.id] = self.items_on_truck.get(item.id, 0) + 1
        item.amount -= 1
        self.current_weight += item.weight
        return True
        

    # returns total value on truck
    def get_value_on_truck(self):
        total_value = 0
        for item in self.items_list:
            if not item.id in self.items_on_truck:
                continue
            total_value += item.value * self.items_on_truck[item.id]
        return total_value

    
    # clears truck and adds items back to warehouse
    def clear_truck(self):
        for item in self.items_list:
            if not item.id in self.items_on_truck:
                continue
            item.amount += self.items_on_truck[item.id]
        self.items_on_truck = {}
        self.current_weight = self.driver_weight


    # formats items on truck to be added to a csv file
    def get_cargo_csv_string(self):
        output = f"\nNew Truck\nDriver-Weight;{self.driver_weight/1000} kg\nItem-Name;Amount\n"
        for item in sorted(self.items_list, key=lambda item: item.id):
            if not item.id in self.items_on_truck:
                continue
            output += f"{item.name};{self.items_on_truck[item.id]}\n"
        return output
