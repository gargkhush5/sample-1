import os
import json
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

class InventoryManager:
    def __init__(self):
        self.inventory = {}  # Format: {item_name: {"price": price, "stock": quantity}}
        self.data_file = "inventory_data.json"
        self.load_inventory()

    def load_inventory(self):
        """Load inventory data from file if it exists"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    self.inventory = json.load(file)
                print(Fore.GREEN + "Inventory data loaded successfully.")
        except Exception as e:
            print(Fore.RED + f"Error loading inventory data: {e}")

    def save_inventory(self):
        """Save inventory data to file"""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.inventory, file, indent=4)
            print(Fore.GREEN + "Inventory data saved successfully.")
        except Exception as e:
            print(Fore.RED + f"Error saving inventory data: {e}")

    def add_item(self):
        name = input(Fore.CYAN + "Enter item name: ").strip()
        # Capitalize the first word of the item name
        name = name.split()
        if name:  # Check if the list is not empty
            name[0] = name[0].capitalize()
        name = " ".join(name)

        if name in self.inventory:
            print(Fore.RED + f"Item '{name}' already exists in inventory.")
            return

        try:
            price = float(input(Fore.CYAN + "Enter item price: ₹"))
            stock = int(input(Fore.CYAN + "Enter item quantity in stock: "))
            if price < 0 or stock < 0:
                print(Fore.RED + "Price and stock cannot be negative.")
                return

            self.inventory[name] = {"price": price, "stock": stock}
            print(Fore.GREEN + f"Item '{name}' added successfully.")
            self.save_inventory()  # Save after adding
        except ValueError:
            print(Fore.RED + "Invalid input. Price must be a number and stock must be an integer.")

    def delete_item(self):
        name = input(Fore.CYAN + "Enter item name to delete: ").strip()

        # Capitalize the first word to match the inventory format
        name_parts = name.split()
        if name_parts:  # Check if the list is not empty
            name_parts[0] = name_parts[0].capitalize()
        name = " ".join(name_parts)

        if name in self.inventory:
            del self.inventory[name]
            print(Fore.GREEN + f"Item '{name}' deleted successfully.")
            self.save_inventory()  # Save after deleting
        else:
            print(Fore.RED + f"Item '{name}' not found in inventory.")

    def update_item(self):
        name = input(Fore.CYAN + "Enter item name to update: ").strip()
        if name not in self.inventory:
            print(Fore.RED + f"Item '{name}' not found in inventory.")
            return

        print(Fore.YELLOW + "\nUpdate Options:")
        print(Fore.YELLOW + "1. Update item name")
        print(Fore.YELLOW + "2. Update item price")
        print(Fore.YELLOW + "3. Update item stock")

        choice = input(Fore.CYAN + "Enter your choice (1-3): ")

        if choice == "1":
            new_name = input(Fore.CYAN + "Enter new item name: ").strip()
            # Capitalize the first word
            new_name = new_name.split()
            if new_name:  # Check if the list is not empty
                new_name[0] = new_name[0].capitalize()
            new_name = " ".join(new_name)

            if new_name in self.inventory:
                print(Fore.RED + f"Item '{new_name}' already exists in inventory.")
            else:
                self.inventory[new_name] = self.inventory.pop(name)
                print(Fore.GREEN + f"Item name changed from '{name}' to '{new_name}'.")
                self.save_inventory()  # Save after updating
        elif choice == "2":
            try:
                new_price = float(input(Fore.CYAN + "Enter new price: ₹"))
                if new_price < 0:
                    print(Fore.RED + "Price cannot be negative.")
                else:
                    self.inventory[name]["price"] = new_price
                    print(Fore.GREEN + f"Price for '{name}' updated to ₹{new_price:.2f}.")
                    self.save_inventory()  # Save after updating
            except ValueError:
                print(Fore.RED + "Invalid input. Price must be a number.")
        elif choice == "3":
            try:
                new_stock = int(input(Fore.CYAN + "Enter new stock quantity: "))
                if new_stock < 0:
                    print(Fore.RED + "Stock cannot be negative.")
                else:
                    self.inventory[name]["stock"] = new_stock
                    print(Fore.GREEN + f"Stock for '{name}' updated to {new_stock}.")
                    self.save_inventory()  # Save after updating
            except ValueError:
                print(Fore.RED + "Invalid input. Stock must be an integer.")
        else:
            print(Fore.RED + "Invalid choice.")

    def display_inventory(self):
        if not self.inventory:
            print(Fore.RED + "Inventory is empty.")
            return

        print(Fore.BLUE + "\nCurrent Inventory:")
        print(Fore.BLUE + "-" * 50)
        print(Fore.BLUE + f"{'Item Name':<20} {'Price':<10} {'Stock':<10}")
        print(Fore.BLUE + "-" * 50)
        
        for name, details in self.inventory.items():
            print(f"{Fore.WHITE}{name:<20} {Fore.YELLOW}₹{details['price']:<9.2f} {Fore.GREEN}{details['stock']:<10}")
        
        print(Fore.BLUE + "-" * 50)


def main():
    inventory = InventoryManager()
    
    while True:
        # Clear screen for better UI (works on Windows, macOS, and Linux)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(Fore.MAGENTA + Style.BRIGHT + "\n✨ Store Inventory Management System ✨")
        print(Fore.CYAN + "=" * 40)
        print(Fore.YELLOW + "1. " + Fore.WHITE + "Add new item")
        print(Fore.YELLOW + "2. " + Fore.WHITE + "Delete item")
        print(Fore.YELLOW + "3. " + Fore.WHITE + "Update item details")
        print(Fore.YELLOW + "4. " + Fore.WHITE + "Display inventory")
        print(Fore.YELLOW + "5. " + Fore.WHITE + "Exit")
        print(Fore.CYAN + "=" * 40)

        choice = input(Fore.GREEN + "\nEnter your choice (1-5): ")

        # Add a temporary pause after operations to show output messages
        if choice in ["1", "2", "3", "4"]:
            # Run the selected operation
            if choice == "1":
                inventory.add_item()
            elif choice == "2":
                inventory.delete_item()
            elif choice == "3":
                inventory.update_item()
            elif choice == "4":
                inventory.display_inventory()
                input(Fore.CYAN + "\nPress Enter to return to menu...")  # Only keep this for display operation
        elif choice == "5":
            inventory.save_inventory()
            print(Fore.MAGENTA + Style.BRIGHT + "\nExiting program. Goodbye! 👋")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")
            input(Fore.CYAN + "\nPress Enter to continue...")  # Keep for invalid choices


if __name__ == "__main__":
    main()