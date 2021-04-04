import re
import sys
import json
import sqlalchemy as db
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
# this script also requires pymysql & cryptography to be installed with the below command
# `pip3 install pymysql cryptography`

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    email = db.Column('email', db.String(125), primary_key=True, nullable=False)
    username = db.Column('username', db.String(125), nullable=True)
    firstName = db.Column('firstName', db.String(125), nullable=True)
    lastName = db.Column('lastName', db.String(125), nullable=True)
    password = db.Column('pass', db.String(40), nullable=False)
    userType = db.Column('userType', db.String(8), nullable=False)

    def __repr__(self):
        return "<User(email='%s', username='%s', firstName='%s', lastName='%s', pass='%s', userType='%s')>" % (
                             self.email, self.username, self.firstName, self.lastName, self.password, self.userType)

class Car(Base):
    __tablename__ = 'Car'

    vin = db.Column('VIN', db.String(17), primary_key=True, nullable=False)
    bodyType = db.Column('bodyType', db.String(40), nullable=True)
    height = db.Column('height', db.Numeric(4,1), nullable=True)
    year = db.Column('year', db.Integer, nullable=True)
    modelName = db.Column('modelName', db.String(40), nullable=True)
    franchiseMake = db.Column('franchiseMake', db.String(40), nullable=True)
    isFleet = db.Column('isFleet', db.String(5), nullable=True)
    isCab = db.Column('isCab', db.String(5), nullable=True)
    isNew = db.Column('isNew', db.String(5), nullable=True)
    listingId = db.Column('listingId', db.Integer, db.ForeignKey("Listing.listingId"), nullable=False)

    def __repr__(self):
        return "<Car(VIN='%s', bodyType='%s', height='%f', modelName='%s', franchiseMake='%s', isFleet='%s', isCab='%s', isNew='%s', listingId='%d)>" % (
                             self.vin, self.bodyType, self.height, self.modelName, self.franchiseMake, self.isFleet, self.isCab, self.isNew, self.listingId)

class Listing(Base):
    __tablename__ = 'Listing'

    listingId = db.Column('listingId', db.Integer, primary_key=True, nullable=False)
    listingDate = db.Column('listingDate', db.Date, nullable=False)
    daysOnMarket = db.Column('daysOnMarket', db.Integer, nullable=True)
    description = db.Column('description', db.String(1000), nullable=True)
    mainPictureURL = db.Column('mainPictureURL', db.String(400), nullable=True)
    majorOptions = db.Column('majorOptions', db.String(1000), nullable=True)
    price = db.Column('price', db.Numeric(9,2), nullable=True)
    dealerEmail = db.Column('dealerEmail', db.String(125), nullable=True)

    def __repr__(self):
        listingId = self.listingId
        listingDate = self.listingDate
        daysOnMarket = self.daysOnMarket
        description = self.description
        mainPictureURL = self.mainPictureURL
        price = self.price
        dealerEmail = self.dealerEmail

        if self.daysOnMarket is None:
            daysOnMarket = -1
        if self.description is None:
            description = "[NULL]"
        if self.mainPictureURL is None:
            mainPictureURL = "[NULL]"
        if self.price is None:
            price = -1.0
        if self.dealerEmail is None:
            dealerEmail = "[NULL]"

        return "<Listing(listingId='%d', listingDate='%s', daysOnMarket='%d', description='%s', mainPictureURL='%s', price='%f', dealerEmail='%s')>" % (
                             listingId, listingDate, daysOnMarket, description, mainPictureURL, price, dealerEmail)

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3307,
    'user': 'admin',
    'password': 'password',
    'database': 'Cars'
}

g_loc = []
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

# set up db connection
db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')
# specify connection string
connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
# connect to database
engine = db.create_engine(connection_str)
connection = engine.connect()

def build_search(page):
    statement = db.select(Car, Listing).join(Listing)

    for f in filter(active_filter, g_filters):
        column = Car
        if f['name'] == 'Year':
            column = Car.year
        elif f['name'] == 'Make':
            column = Car.franchiseMake
        elif f['name'] == 'Model':
            column = Car.modelName
        elif f['name'] == 'Price':
            column = Car.franchiseMake
        elif f['name'] == 'New':
            column = Car.franchiseMake
        elif f['name'] == 'Dealer ZIP':
            column = Car.franchiseMake
        else:
            column = Listing.price
        
        if f['relationship'] == ">":
            statement = statement.where(column > parse(f['value']))
        elif f['relationship'] == ">=":
            statement = statement.where(column >= parse(f['value']))
        elif f['relationship'] == "=":
            val = 0
            if f['f_type'] == "equality":
                val = f['value']
            elif f['f_type'] == "range":
                val = parse(f['value'])
            elif f['f_type'] == "boolean":
                val = parse(f['value']) == 1
            statement = statement.where(column == val)
        elif f['relationship'] == "!=":
            val = 0
            if f['f_type'] == "equality":
                val = f['value']
            elif f['f_type'] == "range":
                val = parse(f['value'])
            elif f['f_type'] == "boolean":
                val = parse(f['value']) == 1
            statement = statement.where(column != val)
        elif f['relationship'] == "<=":
            statement = statement.where(column <= parse(f['value']))
        elif f['relationship'] == "<":
            statement = statement.where(column < parse(f['value']))
    
    return statement.limit(10).offset((page - 1) * 10)

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
    # login()
    main()

#get the user to sign up or log into an account
def login():
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

            new_user = User(email=g_email, username=g_username, firstName=g_firstname, lastName=g_lastname, password=g_password, userType=userType)

            session = Session(engine)
            session.add(new_user)
            session.commit()

            break
        elif (selection == 2):

            g_username = ""
            g_password = ""

            bad_info_repeat = True

            while(bad_info_repeat):
                f_username = input("username: ")
                f_password = input("password: ")

                error_because_of_bad_password = 0

                session = Session(engine)
                results = session.query(User).filter_by(username=str(f_username)).all()
                session.close()

                if (len(results) == 1):
                    if (f_password != results[0].password):
                        print("Incorrect password.")
                        error_because_of_bad_password = 1
                        continue
                    else:
                        g_username = f_username
                        g_password = f_password
                        bad_info_repeat = False
                    
                if (error_because_of_bad_password == 0 and g_username == ""):
                   print("user not found")
                   continue
            break
            
        elif (selection == 0):
            continue
        elif (selection == -1):
            continue
    
    print("Login successful! Welcome to Ottotradr,", g_username)

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

    page = 1

    while (1):
        print("")
        sys.stdout.write("\rSearching (this may take some time)")

        options = []
        option_ids = []
        session = Session(engine, future=True)
        statement = build_search(page)
        result = session.execute(statement).all()
        session.close()

        sys.stdout.write("\rSelect a listing to view it in detail, save it, or buy it. [Page {page:d}]\n".format(page=page))
        sys.stdout.flush()

        for car, listing in result:
            option_ids.append(car.listingId)
            options.append(car.franchiseMake + " " + car.modelName + " [$" + str(listing.price) + "]")
        options.extend(["Previous Page", "Next Page"])

        selection = get_input(options)
        if (selection > 0 and selection <= len(options) - 2):
            detail(option_ids[selection - 1])
            continue
        elif (selection == len(options) - 1):
            if (page > 1):
                page -= 1
            continue
        elif (selection == len(options)):
            if (len(result) == 10):
                page += 1
            continue
        elif (selection == 0):
            nav_up()
            return
        else:
            clear_nav()
            main()
            return

def detail(l_id):
    nav_down("listing_detail")
    
    session = Session(engine, future=True)
    statement = db.select(Car, Listing).join(Listing).where(Car.listingId == l_id)
    result = session.execute(statement).first()

    print("")
    print("Make: " + result.Car.franchiseMake)
    print("Model: " + result.Car.modelName)
    print("Year: " + str(result.Car.year))
    print("Price: " + str(result.Listing.price))
    print("New: " + result.Car.isNew)
    print("VIN: " + result.Car.vin)
    options = []

    while (1):
        owned = False
        saved = False

        if (owned):
            options = ["Edit Listing", "Remove Listing"]
        else:
            options = ["Purchase Vehicle"]
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

                # delete Car
                session = Session(engine, future=True)
                statement = db.delete(Car).where(Car.listingId == l_id)
                session.execute(statement)
                # delete Listing
                session = Session(engine, future=True)
                statement = db.delete(Listing).where(Listing.listingId == l_id)
                session.execute(statement)
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
        active_filters = filter(active_filter, g_filters)
        options = []
        option_names = []
        for f in active_filters:
            option_names.append(f["name"])
            options.append(f["name"] + " " + f["relationship"] + " " + f["value"])

        if len(options) == 0:
            print("No active filters; returning to search.")
            nav_up()
            return

        selection = get_input(options)
        if selection > 0 and selection <= len(options):
            for f in g_filters:
                if (f["name"] == option_names[selection - 1]["name"]):
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
        prompt1 += "'>', '>=', '=', '!=', '<', '<='"
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