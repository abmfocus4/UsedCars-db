import re
import json

g_loc = []

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
        #check if input is a number for menu
        int(input)
        return int(input)
    except ValueError:
        return 0 if input == "b" else -1

def list_options(options):
    print("")
    for index, option in enumerate(options):
        print(str(index + 1) + ". " + option)

def get_input(options):
    list_options(options)
    selection = parse(input("Select an option: "))
    while (selection < -1 or selection > len(options)):
        print("Invalid input.")
        list_options(prompt, options)
        selection = parse(input("Select an option: "))
    return selection

def clear_nav():
    g_loc = []

def nav_down(level):
    g_loc.append(level)
    get_loc()

def nav_up():
    g_loc.pop()
    get_loc()


def get_loc():
    location = ""
    for level in g_loc:
        location += "/" + level
    print("")
    print(location)

def active_filter(f):
    return f["active"]

#navigate throught the app
def main():
    options = ["Search Listings", "Create Listing", "View Your Listings", "View Saved Listings"]
    nav_down("main")
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
            clear_nav()
            main()
            return

#starting point of the cli
def startup():
    print("Welcome to Ottotradr: a used car sales platform that's definitely not affiliated with Auto Trader.")
    print("Navigate the application using the prompts, using 'q' to quit & 'b' to navigate back.")
    login()
    main()

#get the user to sign up or log into an account
def login():

    #add ending ] at login()
    g_user = """ [
        {
        "emailAddress":"bmalapat@uwaterloo.ca",
        "username":"megAdmin",
        "firstName":"Mag",
        "lastName":"Alapati",
        "password":"Admin1$a",
        "userType":"Admin",
        "phoneNumber": "no",
        "postalcode":"no"
    },
    {
        "emailAddress":"s2ishraq@uwaterloo.ca",
        "username":"shwapAdmin",
        "firstName":"Shwapneel",
        "lastName":"Ishraq",
        "password":"Admin1$a",
        "userType":"Admin",
        "phoneNumber": "no",
        "postalcode":"no"
    },
    {
        "emailAddress":"connor.peter.barker@uwaterloo.ca",
        "username":"connorAdmin",
        "firstName":"Connor",
        "lastName":"Barker",
        "password":"Admin1!a",
        "userType":"Admin",
        "phoneNumber": "no",
        "postalcode":"no"
    }"""

    options = ["Sign Up", "Log In"]
    g_username = "user"
    pw1 = "1"
    pw2 = "2"
    email = "example@example.com"
    nav_down("login")

    while (1):
        selection = get_input(options)
        if (selection == 1):
            userType = "select"
            while ( (userType != 'Customer') and (userType != 'Dealer') ):
                 userType = input("Are you a 'Customer' or a 'Dealer' (Spell Customer or Dealer exactly the same as this)?: ")

            g_username = input("enter your username: ")
            g_firstname = input("enter your firstname: ")
            g_lastname = input("enter your lastname: ")
            while (pw1 != pw2):
                password_check = False
                while ( not password_check ):
                   pw1 = input("Enter your password: (minimum 8 character, 1 uppercase, 1 lowercase, 1 number, 1 special): ")
                   password_check = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",pw1)
                   #password_check = True
                pw2 = input("Confirm password: ")
                if (pw1 != pw2):
                    print("Passwords do not match.")
            g_password = pw1

            check_email = False
            while ( not check_email):
                g_email = input("enter your email: ")
                check_email = re.search("^\S+@\S+\.\S+$",g_email)

            is_valid_phone = False
            while ( not is_valid_phone ):
                g_phone = input("Enter your phone number, if you don't have one then enter no: ")
                if ( ( g_phone.isnumeric() and len(g_phone)<=15 ) or ( g_phone == "no" ) ):
                   is_valid_phone = True

            is_valid_postal = False
            while ( not is_valid_postal ):
                g_postal = input("Enter your postal code, if you don't have one then enter no: ")
                if ( ( len(g_postal)<=32 ) or ( g_postal == "no" ) ):
                   is_valid_postal = True       
            
            user_info_json = ',{"username":\"' + g_username + "\",\"fistname\":\"" + g_firstname + "\",\"lastname\":\"" + g_lastname +"\",\"password\":\"" + g_password + "\",\"email\":\"" + g_email + "\",\"phone\":\"" + g_phone + "\",\"postal code\":\"" + g_postal + '\"}'

            print(user_info_json)

            g_user += user_info_json 

            break
        elif (selection == 2):

            g_username = ""
            g_password = ""

            bad_info_repeat = True

            while(bad_info_repeat):
                f_username = input("username: ")
                f_password = input("password: ")

                all_users = g_user + "]"
                all_users_json_formatted = json.loads(all_users)

                error_because_of_bad_password = 0

                for i in all_users_json_formatted:
                
                    if ( i["username"] == f_username ):
                        if ( i["password"] != f_password ):
                            print(" incorrect password ")
                            error_because_of_bad_password = 1
                            login()
                        else:
                            g_username = f_username
                            g_password = f_password
                            bad_info_repeat = False
                    
                if (error_because_of_bad_password == 0 and g_username == ""):
                   print("user not found")
                   login()
            break
            
        elif (selection == 0):
            continue
        elif (selection == -1):
            continue
    
    print("Login successful!")

    nav_up()

def saved_listings():
    nav_down("saved_listings")

    if (len(g_saved_listings) == 0):
        print("Looks like you haven't saved any listings! You can do so from the search page.")
    else:
        while(1):
            options = []
            for l in g_saved_listings:
                g_l = g_listings[l]
                options.append(g_l["make"] + " " + g_l["model"])
            selection = get_input(options)
            if (selection > 0 and selection <= len(options)):
                detail(g_saved_listings[selection - 1])
            elif (selection == 0):
                break
            elif (selection == -1):
                clear_nav()
                main()
                return
    
    nav_up()

def owned_listings():
    nav_down("owned_listings")
    if (len(g_owned_listings) == 0):
        print("Looks like you don't have any listings! You can create them from the main page.")
    else:
        while (1):
            options = []
            for i, l in enumerate(g_owned_listings):
                listing = g_listings[l]
                options.append(listing["make"] + " " + listing["model"])
            selection = get_input(options)
            if (selection > 0 and selection <= len(options)):
                detail(g_owned_listings[selection - 1])
            elif (selection == 0):
                break
            elif (selection == -1):
                clear_nav()
                main()
                return

    nav_up()
        
def new_listing():
    nav_down("new_listing")
    print("")
    make = input("Enter vehicle make: ")
    model = input("Enter vehicle model: ")
    year = input("Enter vehicle year: ")
    price = input("Enter desired list price: ")
    new = input("Is this vehicle new (y/n): ")

    is_valid_vin = False
    while ( not is_valid_vin ):
        vin = input("Enter vehicle VIN number: ")
        if ( vin.isnumeric() and len(vin) >= 11 and len(vin) <= 17 ):
            is_valid_vin = True

    print("You are about to list the following vehicle for sale:")
    print("Make: " + make)
    print("Model: " + model)
    print("Year: " + year)
    print("Price: " + price)
    print("New: " + ("True" if new == "y" else "False"))
    print("VIN: " + vin)

    confirm = input("Please type 'confirm' to list this vehicle, or any other input to cancel: ")

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
    
    nav_up()
    return

def search():
    nav_down("search")
    options = ["Add Filters", "View & Remove Filters", "Display Results"]
    while (1):
        selection = get_input(options)
        if (selection == 1):
            addfilters()
        elif (selection == 2):
            removefilters()
        elif (selection == 3):
            display()
        elif (selection == 0):
            break
        else:
            clear_nav()
            main()
            return

    nav_up()

def display():
    nav_down("search_results")
    while (1):
        print("")
        print("Select a listing to view it in detail, save it, or buy it.")

        options = []
        for listing in g_listings:
            options.append(listing["make"] + " " + listing["model"])
        selection = get_input(options)
        if (selection > 0 and selection <= len(options)):
            detail(selection - 1)
        elif (selection == 0):
            nav_up()
            return
        else:
            clear_nav()
            main()
            return

def detail(l_id):
    nav_down("listing_detail")
    l = g_listings[l_id]
    print("")
    print("Make: " + str(l["make"]))
    print("Model: " + str(l["model"]))
    print("Year: " + str(l["year"]))
    print("Price: " + str(l["price"]))
    print("New: " + str(l["new"]))
    print("VIN: " + str(l["vin"]))
    options = []

    while (1):
        owned = l_id in g_owned_listings
        saved = l_id in g_saved_listings

        if (owned):
            options = ["Edit Listing", "Remove Listing"]
        else:
            if (saved):
                options = ["Unsave Listing", "Purchase Vehicle"]
            else:
                options = ["Save Listing", "Purchase Vehicle"]
        selection = get_input(options)
        if (owned):
            if (selection == 1):
                editlisting(l_id)
            elif (selection == 2):
                removelisting(l_id)
                nav_up()
                return
            elif (selection == 0):
                nav_up()
                return
            else:
                clear_nav()
                main()
                return
        else:
            if (selection == 1):
                if (saved):
                    g_saved_listings.remove(l_id)
                    print("Removed from saved listings.")
                else:
                    g_saved_listings.append(l_id)
                    print("Listing saved; view it from the main page.")
            elif (selection == 2):
                vehicle = g_listings[l_id]
                g_listings.remove(vehicle)
                print("Vehicle purchased! Thank you for your patronage.")
                nav_up()
                return
            elif (selection == 0):
                nav_up()
                return
            else:
                clear_nav()
                main()
                return

def removelisting(l_id):
    nav_down("remove_listing")
    print("")
    print("VIN: " + str(g_listings[l_id]["vin"]))
    confirm = input("Enter this vehicle's VIN to confirm listing deletion: ")
    if (confirm == str(g_listings[l_id]["vin"])):
        g_listings.remove(g_listings[l_id])
        g_owned_listings.remove(l_id)
        print("Listing removed.")
    else:
        print("Listing not removed.")

    nav_up()

def editlisting(l_id):
    nav_down("edit_listing")
    l = g_listings[l_id]
    print("")
    print("Make: " + str(l["make"]))
    print("Model: " + str(l["model"]))
    print("Year: " + str(l["year"]))
    print("Price: " + str(l["price"]))
    print("New: " + str(l["new"]))
    print("VIN: " + str(l["vin"]))
    options = []
    for f in g_filters:
        options.append(f["name"])

    options.append("View Details")
    
    while (1):
        selection = get_input(options)
        if (selection > 0 and selection < len(options)):
            value = input("Enter a new value for " + options[selection - 1] + ": ")
            l[options[selection - 1].lower()] = value
        elif (selection == len(options)):
            print("Make: " + str(l["make"]))
            print("Model: " + str(l["model"]))
            print("Year: " + str(l["year"]))
            print("Price: " + str(l["price"]))
            print("New: " + str(l["new"]))
            print("VIN: " + str(l["vin"]))
        elif (selection == 0):
            break
        else:
            clear_nav()
            main()
            break

    nav_up()

def removefilters():
    nav_down("remove_filters")
    print("Select a filter to remove it")
    while (1):
        active_filters = filter(active_filter, g_filters);
        for i, f in enumerate(active_filters):
            print(str(i + 1) + ". " + f["name"] + " " + f["relationship"] + " " + f["value"])

        if (len(active_filters) == 0):
            print("No active filters; returning to search.")
            nav_up()
            return

        selection = parse(input("Select an option: "))
        if (selection > 0 and selection <= len(active_filters)):
            for f in g_filters:
                if (f["name"] == active_filters[selection - 1]["name"]):
                    f["active"] = 0
                    break
        elif (selection == 0):
            break
        elif (selection == -1):
            clear_nav()
            main()
            return

    nav_up()

def editfilter(index):
    nav_down("edit_filter")
    f = g_filters[index]
    prompt1 = "Enter one of "
    prompt2 = "Select a value for this filter (" + f["name"] + "): "
    if (f["f_type"] == "equality"):
        prompt1 += "'=', '!='"
    elif (f["f_type"] == "range"):
        prompt1 += "'>', '>=', '='. '!=', '<', '<='"
    else:
        prompt1 += "'1', '0'"
    
    prompt1 += " for the " + f["name"] + " filter operator: "

    rel = input(prompt1)
    val = input(prompt2)

    f["active"] = 1
    f["relationship"] = rel
    f["value"] = val

    nav_up()
    return

def addfilters():
    nav_down("add_filters")
    options = []
    for f in g_filters:
        options.append(f["name"])
    while (1):
        selection = get_input(options)
        if (selection > 0 and selection <= len(g_filters)):
            editfilter(selection - 1)
        elif (selection == 0):
            nav_up()
            break
        elif (selection == -1):
            clear_nav()
            main()
            return
        else:
            print("Invalid input.")

startup()