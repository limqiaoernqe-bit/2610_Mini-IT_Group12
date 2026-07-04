# Inventory System
class Inventory:
    def __init__(self):
        self.items = []


    # Add item to inventory
    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)
            print(f"Picked up: {item}")
        else:
            print(f"You already have {item} in your inventory.")


    # Check if item is in inventory
    def has_item(self, item):
        return item in self.items


    # Remove item from inventory
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed: {item} from inventory.")
        else:
            print(f"{item} is not in your inventory.")


    # Display inventory items
    def show_inventory(self):
        if self.items:
            print("Inventory:", self.items)
        else:
            print("Your inventory is empty.")


    # Use item on a target
    def use_item(self, item, target):
        if self.has_item(item):


            if item == target.required_key:
                self.remove_item(item)
                target.unlock()
                print(f"{target.name} unlocked with {item}!")
            else:
                print(f"{item} used, but nothing happened.")


        else:
            print(f"You don't have {item} in your inventory.")


game_inventory = Inventory()


JANITOR_KEY = "JANITOR_KEY"
ROOM_210_KEY = "ROOM_210_KEY"
ROOM_206_KEY = "ROOM_206_KEY"
SECURITY_BADGE = "SECURITY_BADGE"
BOLT_CUTTER = "BOLT_CUTTER"

# Level 1 keys 
ROOM116_KEY = "ROOM116_KEY"
ROOM116_117_CODE = "ROOM116_117_CODE"
EXIT_DOOR_KEY = "EXIT_DOOR_KEY"
ROOM117_KEY = "ROOM117_KEY"
