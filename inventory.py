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




# Keys
JANITOR_KEY = "janitor_key"
ROOM_210_KEY = "room_210_key"
ROOM_206_KEY = "room_206_key"
SECURITY_BADGE = "security_badge"
EXIT_KEY = "exit_key"


# Tools
LOCK_CUTTER = "lock_cutter"
SCREWDRIVER = "screwdriver"


# Weapon Pieces
WEAPON_1 = "weapon_piece_1"
WEAPON_2 = "weapon_piece_2"
WEAPON_3 = "weapon_piece_3"




# TEST / DEMO
if __name__ == "__main__":


    inventory = Inventory()


    inventory.show_inventory()


    inventory.add_item(JANITOR_KEY)
    inventory.add_item(ROOM_206_KEY)
    inventory.add_item(LOCK_CUTTER)
    inventory.add_item(SCREWDRIVER)


    inventory.add_item(JANITOR_KEY)


    inventory.show_inventory()


    print("Has janitor key?", inventory.has_item(JANITOR_KEY))
    print("Has room 210 key?", inventory.has_item(ROOM_210_KEY))
    print("Has room 206 key?", inventory.has_item(ROOM_206_KEY))
    print("Has security badge?", inventory.has_item(SECURITY_BADGE))

    inventory.remove_item(LOCK_CUTTER)


    inventory.show_inventory()