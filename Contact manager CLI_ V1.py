'''
This is the main project for Shadow Build (python) 
where I, Nicholas Liphapang, will be building a contact manager
with the skills I will be learning during this sprint.

I shall be adding new features, not building it in one go.
'''

# WEEK 1
import os

# Get the folder where this script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# File path for contacts
CONTACTS_FILE = os.path.join(SCRIPT_DIR, "contacts.txt")

# Monday - add contact to text file (name, phone, email).
def add_contact():
    # Get user input
    name = input("Enter name: ").strip().capitalize()
    phone = input("Enter phone number (eg +266 59924202): ").strip()
    email = input("Enter email address: ").strip()

    #Validation
    if not name:
        print("Error: Name is required. Contact not saved.")
        return
    if not phone:
        print("Error: Phone number is required. Contact not saved.")
        return
    
    
    # Append to file 
    with open(CONTACTS_FILE, "a") as file:
        file.write(f"{name},{phone},{email}\n")
        
    print(f"Contact for {name} saved successfully!")

#Tuesday-View all contacts, search by name.

def view_contacts():    # ADD BETTER OUTPUT DISPLAY WHEN REFINING!!!!!!!!!!
    #opening contacts file and reading from it.
    with open(CONTACTS_FILE, "r") as file:
        contacts = file.readlines()
    
    # Display all contacts
    for contact in contacts:
        print(contact.strip()) # Avoid new lines being created
    
    # Error handling
    if not contacts: print("No contacts found")

def search_contact():
    search_name = input("Enter the name you want to search: ").strip().capitalize()

    with open(CONTACTS_FILE, "r") as file:
        contacts = file.readlines()

        for contact in contacts:
            name, phone, email = contact.split(",")

            if search_name in contact:
                print(f"Name: {name}  \n phone: {phone} \n email: {email}")
                break

        else: 
            print("Contact not found, try again")  

def main():
    while True:
        print("\n" + "="*20)
        print("CONTACT MANAGER")
        print("="*20)
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()