g_username = ""
g_password = ""
g_listings = [
    {
        "l_id": 0,
        "make": "Chevrolet",
        "model": "Impala Sport Coupe",
        "year": 1975,
        "price": 15400,
        "new": False,
        "vin": "4Y1SL65848Z411439"
    },
    {
        "l_id": 1,
        "make": "Ford",
        "model": "F150",
        "year": 2004,
        "price": 7500,
        "new": False,
        "vin": "4Y1SL41828Z411927"
    },
    {
        "l_id": 2,
        "make": "Ford",
        "model": "Bronco Classic",
        "year": 1969,
        "price": 38000,
        "new": False,
        "vin": "4Y1VC72847Z033278"
    }
]
g_owned_listings = []
g_saved_listings = []
g_filters = [
    {
        "name": "Year",
        "f_type": "range",
        "relationship": "",
        "value": "",
        "active": False
    },
    {
        "name": "Make",
        "f_type": "equality",
        "relationship": "",
        "value": "",
        "active": False
    },
    {
        "name": "Model",
        "f_type": "equality",
        "relationship": "",
        "value": "",
        "active": False
    },
    {
        "name": "Price",
        "f_type": "range",
        "relationship": "",
        "value": "",
        "active": False
    },
    {
        "name": "New",
        "f_type": "boolean",
        "relationship": "",
        "value": "",
        "active": False
    },
    {
        "name": "Dealer ZIP",
        "f_type": "equality",
        "relationship": "",
        "value": "",
        "active": False
    },
    {
        "name": "Listing Age",
        "f_type": "range",
        "relationship": "",
        "value": "",
        "active": False
    }
]

def parse(input):
    try:
        int(input)
        return int(input)
    except ValueError:
        return 0 if input == "b" else -1

def list_options(options):
    print("")
    print("Options:")
    for index, option in enumerate(options):
        print(str(index + 1) + ". " + option)

def get_input(options):
    list_options(options)
    selection = parse(raw_input("Select an option: "))
    while (selection < -1 or selection > len(options)):
        print("Invalid input.")
        list_options(prompt, options)
        selection = parse(raw_input("Select an option: "))
    return selection

def active_filter(f):
    return f["active"]

def main():
    options = ["Search Listings", "Create Listing", "View Your Listings", "View Saved Listings"]

    while (1):
        selection = get_input(options)
        if (selection == 1):
            search()
        elif (selection == 2):
            new_listing()
        elif (selection == 3):
            owned_listings()
        elif (selection == 4):
            saved_listings()
        elif (selection == 0):
            continue
        else:
            main()
            return

def startup():
    print("Welcome to Ottotradr: a used car sales platform that's definitely not affiliated with Auto Trader.")
    print("Navigate the application using the prompts, using 'q' to quit & 'b' to navigate back.")
    # login()
    main()

def login():
    print("")
    g_username = raw_input("username: ")
    g_password = raw_input("password: ")

    while (g_username != "root" and g_password != "password"):
        print("Invalid credentials.")
        g_username = raw_input("username:")
        g_password = raw_input("password:")

def saved_listings():
    print("")
    print("Looks like you haven't saved any listings! You can do so from the search page.")

def owned_listings():
    print("")
    if (len(g_owned_listings) == 0):
        print("Looks like you don't have any listings! You can create them from the main page.")
    else:
        options = []
        for i, l in enumerate(g_owned_listings):
            listing = g_listings[l]
            options.append(listing["make"] + " " + listing["model"])
        selection = get_input(options)
        if (selection > 0 and selection <= len(options)):
            detail(g_owned_listings[selection - 1])
        elif (selection == 0):
            return
        else:
            main()
            return
        
def new_listing():
    print("")
    make = raw_input("Enter vehicle make: ")
    model = raw_input("Enter vehicle model: ")
    year = raw_input("Enter vehicle year: ")
    price = raw_input("Enter desired list price: ")
    new = raw_input("Is this vehicle new (y/n): ")
    vin = raw_input("Enter vehicle VIN number: ")

    print("You are about to list the following vehicle for sale:")
    print("Make: " + make)
    print("Model: " + model)
    print("Year: " + year)
    print("Price: " + price)
    print("New: " + ("True" if new == "y" else "False"))
    print("VIN: " + vin)

    confirm = raw_input("Please type 'confirm' to list this vehicle, or any other input to cancel: ")

    if (confirm == "confirm"):
        g_listings.append({
            "l_id": len(g_listings),
            "make": make,
            "model": model,
            "year": year,
            "price": price,
            "new": True if new == "y" else False,
            "vin": vin
        })
        g_owned_listings.append(len(g_listings) - 1)
        print("Car listed for sale!")
    else:
        print("Listing cancelled.")
    
    return

def search():
    print("")
    options = ["Filter By", "View & Remove Filters", "Search"]
    while (1):
        selection = get_input(options)
        if (selection == 1):
            filterby()
        elif (selection == 2):
            removefilters()
        elif (selection == 3):
            display()
        elif (selection == 0):
            break
        else:
            main()
            return

def display():
    print("")
    options = []
    for listing in g_listings:
        options.append(listing["make"] + " " + listing["model"])
    while (1):
        print("Select a listing to view it in detail, save it, or buy it.")
        selection = get_input(options)
        if (selection > 0 and selection <= len(options)):
            detail(selection - 1)
        elif (selection == 0):
            return
        else:
            main()
            return

def detail(l_id):
    print("")
    l = g_listings[l_id]
    print("Make: " + str(l["make"]))
    print("Model: " + str(l["model"]))
    print("Year: " + str(l["year"]))
    print("Price: " + str(l["price"]))
    print("New: " + str(l["new"]))
    print("VIN: " + str(l["vin"]))
    options = []
    owned = l_id in g_owned_listings
    if (owned):
        options = ["Edit Listing", "Remove Listing"]
    else:
        options = ["Save Listing", "Purchase Vehicle"]
    while (1):
        selection = get_input(options)
        if (owned):
            if (selection == 1):
                print("Edit listing would open here.")
            elif (selection == 2):
                print("Remove listing would open here.")
            else:
                return
        else:
            if (selection == 1):
                print("Listing saved; view it from the main page.")
            elif (selection == 2):
                vehicle = g_listings[l_id]
                g_listings.remove(vehicle)
                print("Vehicle purchased! Thank you for your patronage.")
                return
            else:
                return

def removefilters():
    print("")
    print("Select a filter to remove it")
    while (1):
        active_filters = filter(active_filter, g_filters);
        for i, f in enumerate(active_filters):
            print(str(i + 1) + ". " + f["name"] + " " + f["relationship"] + " " + f["value"])

        if (len(active_filters) == 0):
            print("No active filters; returning to search.")
            return

        selection = parse(raw_input("Select an option: "))
        if (int(selection) < 1 or int(selection) > len(active_filters)):
            print("Invalid input.")
            continue
        elif (selection == 0):
            return
        elif (selection == -1):
            main()
            return
        else:
            for f in g_filters:
                if (f["name"] == active_filters[selection - 1]["name"]):
                    f["active"] = 0
                    break

def editfilter(index):
    print("")
    f = g_filters[index]
    prompt1 = "Enter one of "
    prompt2 = "Select a value for this relationship: "
    if (f["f_type"] == "equality"):
        prompt1 += "'=', '!='"
    elif (f["f_type"] == "range"):
        prompt1 += "'>', '>=', '='. '!=', '<', '<='"
    else:
        prompt1 += "'1', '0'"
    
    prompt1 += " for the filter relationship: "

    rel = raw_input(prompt1)
    val = raw_input(prompt2)

    f["active"] = 1
    f["relationship"] = rel
    f["value"] = val

    return

def filterby():
    print("")
    options = []
    for f in g_filters:
        options.append(f["name"])
    while (1):
        selection = get_input(options)
        if (selection > 0 and selection <= len(g_filters)):
            editfilter(selection - 1)
        elif (selection == 0):
            break
        elif (selection == -1):
            main()
            return
        else:
            print("Invalid input.")

startup()