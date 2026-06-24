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


JANITOR_KEY = "janitor_key"
ROOM_210_KEY = "room_210_key"
ROOM_206_KEY = "room_206_key"

# Level 1 keys 
SECURITY_BADGE = "security_badge"
ROOM116_KEY = "room116_key"
ROOM117_KEY = "room117_key"
ROOM116_117_CODE = "room116_117_code"
EXIT_DOOR_KEY = "exit_door_key"


# Tools
LOCK_CUTTER = "lock_cutter"
SCREWDRIVER = "screwdriver"
