import re
import sys
import json
import datetime
import sqlalchemy as db
from sqlalchemy.orm import Session, aliased
from sqlalchemy.ext.declarative import declarative_base
# this script also requires pymysql & cryptography to be installed with the below command
# `pip3 install pymysql cryptography`
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import graphviz 

Base = declarative_base()

# Setup for the objects representing SQL relations

class User(Base):
    __tablename__ = 'User'

    email = db.Column('email', db.String(125), primary_key=True, nullable=False)
    firstName = db.Column('firstName', db.String(125), nullable=True)
    lastName = db.Column('lastName', db.String(125), nullable=True)
    password = db.Column('pass', db.String(40), nullable=False)
    userType = db.Column('userType', db.String(14), nullable=False)

    def __repr__(self):
        return "<User(email='%s', firstName='%s', lastName='%s', pass='%s', userType='%s')>" % (
                             self.email, self.firstName, self.lastName, self.password, self.userType)

class Car(Base):
    __tablename__ = 'Car'

    vin = db.Column('VIN', db.String(17), primary_key=True, nullable=False)
    bodyType = db.Column('bodyType', db.String(40), nullable=True)
    height = db.Column('height', db.Numeric(4,1), nullable=True)
    width = db.Column('width', db.Numeric(4,1), nullable=True)
    length = db.Column('length', db.Numeric(4,1), nullable=True)
    color = db.Column('color', db.String(125), nullable=False)
    year = db.Column('year', db.Integer, nullable=True)
    modelName = db.Column('modelName', db.String(40), nullable=True)
    franchiseMake = db.Column('franchiseMake', db.String(40), nullable=True)
    isFleet = db.Column('isFleet', db.String(5), nullable=True)
    isCab = db.Column('isCab', db.String(5), nullable=True)
    listingId = db.Column('listingId', db.Integer, db.ForeignKey("Listing.listingId"), nullable=False)

    def __repr__(self):
        return "<Car(VIN='%s', bodyType='%s', height='%f', width='%f', length='%f', color='%2', modelName='%s', franchiseMake='%s', isFleet='%s', isCab='%s', listingId='%d)>" % (
                             self.vin, self.bodyType, self.height, self.width, self.length, self.color, self.modelName, self.franchiseMake, self.isFleet, self.isCab, self.listingId)

class Listing(Base):
    __tablename__ = 'Listing'

    listingId = db.Column('listingId', db.Integer, primary_key=True, nullable=False)
    listingDate = db.Column('listingDate', db.Date, nullable=False)
    daysOnMarket = db.Column('daysOnMarket', db.Integer, nullable=True)
    description = db.Column('description', db.String(1000), nullable=True)
    mainPictureURL = db.Column('mainPictureURL', db.String(400), nullable=True)
    majorOptions = db.Column('majorOptions', db.String(1000), nullable=True)
    price = db.Column('price', db.Numeric(9,2), nullable=True)
    activeListing = db.Column('activeListing', db.String(5), nullable=True)
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

class Engine(Base):
    __tablename__ = 'Engine'

    vin = db.Column('VIN', db.String(17), db.ForeignKey("Car.VIN"), primary_key=True, nullable=False)
    engineCylinders = db.Column('engineCylinders', db.String(40), nullable=True)
    engineDisplacement = db.Column('engineDisplacement', db.Numeric(8,3), nullable=True)
    engineType = db.Column('engineType', db.String(40), nullable=True)
    horsepower = db.Column('horsepower', db.Numeric(5,2), nullable=True)
    transmission = db.Column('transmission', db.String(40), nullable=True)
    transmissionDisplay = db.Column('transmissionDisplay', db.String(125), nullable=True)
    power = db.Column('power', db.String(125), nullable=True)

class FuelSpecs(Base):
    __tablename__ = 'FuelSpecs'

    vin = db.Column('VIN', db.String(17), db.ForeignKey("Car.VIN"), primary_key=True, nullable=False)
    fuelTankVolume = db.Column('fuelTankVolume', db.Numeric(4,1), nullable=True)
    fuelType = db.Column('fuelType', db.String(40), nullable=True)
    cityFuelEconomy = db.Column('cityFuelEconomy', db.Numeric(5,2), nullable=True)
    highwayFuelEconomy = db.Column('highwayFuelEconomy', db.Numeric(5,2), nullable=True)

class TrimPackage(Base):
    __tablename__ = 'TrimPackage'

    vin = db.Column('VIN', db.String(17), db.ForeignKey("Car.VIN"), primary_key=True, nullable=False)
    trimId = db.Column('trimId', db.Numeric(5,0), nullable=True)
    trimName = db.Column('trimName', db.String(125), nullable=True)

class Interior(Base):
    __tablename__ = 'Interior'

    vin = db.Column('VIN', db.String(17), db.ForeignKey("Car.VIN"), primary_key=True, nullable=False)
    backLegroom = db.Column('backLegroom', db.Numeric(4,1), nullable=True)
    frontLegroom = db.Column('frontLegroom', db.Numeric(4,1), nullable=True)
    interiorColor = db.Column('interiorColor', db.String(125), nullable=True)
    maximumSeating = db.Column('maximumSeating', db.Integer, nullable=True)

class WheelSystem(Base):
    __tablename__ = 'WheelSystem'

    vin = db.Column('VIN', db.String(17), db.ForeignKey("Car.VIN"), primary_key=True, nullable=False)
    wheelSystem = db.Column('wheelSystem', db.String(3), nullable=True)
    wheelSystemDisplay = db.Column('wheelSystemDisplay', db.String(40), nullable=True)
    wheelbase = db.Column('wheelbase', db.Numeric(4,1), nullable=True)

class DepreciationFactors(Base):
    __tablename__ = 'DepreciationFactors'

    vin = db.Column('VIN', db.String(17), db.ForeignKey("Car.VIN"), primary_key=True, nullable=False)
    frameDamaged = db.Column('frameDamaged', db.String(5), nullable=True)
    hasAccidents = db.Column('hasAccidents', db.String(5), nullable=True)
    salvage = db.Column('salvage', db.String(5), nullable=True)
    savingsAmount = db.Column('savingsAmount', db.Numeric(7,2), nullable=True)

class Appointment(Base):
    __tablename__ = 'Appointment'

    appointmentNumber = db.Column('appointmentNumber', db.Integer, primary_key=True, nullable=False)
    dealerEmail = db.Column('dealerEmail', db.String(125), db.ForeignKey("User.email"), primary_key=True, nullable=False)
    customerEmail = db.Column('customerEmail', db.String(125), db.ForeignKey("User.email"), primary_key=True, nullable=False)
    appointmentDateTime = db.Column('appointmentDateTime', db.DateTime, nullable=False)
    information = db.Column('information', db.String(400), nullable=True)
    active = db.Column('active', db.String(5), nullable=True)
    listingId = db.Column('listingId', db.Integer, db.ForeignKey("Listing.listingId"), nullable=False)

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3307,
    'user': 'admin',
    'password': 'password',
    'database': 'Cars'
}

# global variables
g_email = None
g_userType = None
g_firstName = None
g_loc = []
g_sorting = [
    {
        "name": "Price",
        "type": "standard",
        "active": False
    },
    {
        "name": "Price",
        "type": "inverted",
        "active": False
    },
    {
        "name": "Year",
        "type": "standard",
        "active": False
    },
    {
        "name": "Year",
        "type": "inverted",
        "active": False
    }
]
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
        "name": "Color",
        "f_type": "equality",
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

# format input for insertion into the database
# e.g. make sure floating point numbers have the
# correct number of digits, strings aren't too
# long, etc
def format_for_db(user_input, input_type, v1=0, v2=0):
    if user_input is None or len(str(user_input)) == 0:
            return None

    if input_type == "string":
        return user_input[:v1] if len(user_input) > v1 else user_input
    elif input_type == "boolean":
        return "True" if user_input else "False"
    elif input_type == "float":
        float_input = 0.0
        max_input = 0.0
        i = 0

        try:
            float_input = float(user_input)
        except ValueError:
            return None

        remainder = float_input % 1
        while i < v1:
            max_input = max_input * 10 + 9
            i += 1
        
        if float_input + 1 > max_input:
            while float_input + 1 > max_input:
                float_input -= float_input % 10
                float_input = float_input / 10
            float_input += remainder

        return round(float_input, v2)
    elif input_type == "integer":
        try:
            int(user_input)
            return int(user_input)
        except ValueError:
            return None

# given either an existing relational object or an id
# (conditionally a listingId or a VIN)
# print out all relevant information pertaining to
# the relation in question
def print_listing(info_type, arg_id=0, arg_object=None):
    ret = False
    vin = 0

    print("")

    if info_type == "car" or info_type == "list" or info_type == "all":
        dbCar = None
        if arg_object:
            dbCar = arg_object
        else:
            session = Session(engine, future=True)
            statement = db.select(Car).where(Car.listingId == arg_id)
            result = session.execute(statement).first()
            session.close()

            if result:
                dbCar = result.Car

        if dbCar:
            print("VIN: " + str(dbCar.vin))
            print("Make: " + str(dbCar.franchiseMake))
            print("Model: " + str(dbCar.modelName))
            print("Body type: " + str(dbCar.bodyType))
            print("Year: " + str(dbCar.year))
            print("Cab: " + str(dbCar.isCab))
            print("")
            vin = dbCar.vin
            ret = True

    if info_type == "listing" or info_type == "list" or info_type == "all":
        dbListing = None
        if arg_object:
            dbListing = arg_object
        else:
            session = Session(engine, future=True)
            statement = db.select(Listing).where(Listing.listingId == arg_id)
            result = session.execute(statement).first()
            session.close()

            if result:
                dbListing = result.Listing
        
        if dbListing:
            print("Posted on: " + str(dbListing.listingDate.strftime("%x")))
            print("Posted by: " + str(dbListing.dealerEmail))
            print("Price: $" + str(dbListing.price))
            print("Description: " + str(dbListing.description))
            print("")
            ret = True

    # automatically retrieve VIN
    arg = vin if info_type == "all" else arg_id

    if arg == 0 and info_type == "all":
        return False
    
    if info_type == "trim" or info_type == "all":
        dbTrimPackage = None
        if arg_object:
            dbTrimPackage = arg_object
        else:
            session = Session(engine, future=True)
            statement = db.select(TrimPackage).where(TrimPackage.vin == arg)
            result = session.execute(statement).first()
            session.close()

            if result:
                dbTrimPackage = result.TrimPackage
        
        if dbTrimPackage:
            print("Trim package: " + str(dbTrimPackage.trimName))
            ret = True
    
    if info_type == "engine" or info_type == "all":
        dbEngine = None
        if arg_object:
            dbEngine = arg_object
        else:
            session = Session(engine, future=True)
            statement = db.select(Engine).where(Engine.vin == arg)
            result = session.execute(statement).first()
            session.close()

            if result:
                dbEngine = result.Engine
        
        if dbEngine:
            print("Engine displacement: " + str(dbEngine.engineDisplacement) + "mL")
            print("Engine type: " + str(dbEngine.engineType))
            print("Engine cylinders: " + str(dbEngine.engineCylinders))
            print("Transmission: " + str(dbEngine.transmission))
            print("Horsepower: " + str(dbEngine.horsepower) + "bhp")
            print("")
            ret = True
    
    if info_type == "interior" or info_type == "all":
        dbInterior = None
        if arg_object:
            dbInterior = arg_object
        else:
            session = Session(engine, future=True)
            statement = db.select(Interior).where(Interior.vin == arg)
            result = session.execute(statement).first()
            session.close()

            if result:
                dbInterior = result.Interior
        
        if dbInterior:
            print("Front legroom: " + str(dbInterior.frontLegroom) + "cm")
            print("Rear legroom: " + str(dbInterior.backLegroom) + "cm")
            print("Interior colour: " + str(dbInterior.interiorColor))
            print("Maximum seating: " + str(dbInterior.maximumSeating))
            print("")
            ret = True
    
    if info_type == "fuel" or info_type == "all":
        dbFuelSpecs = None
        if arg_object:
            dbFuelSpecs = arg_object
        else:
            session = Session(engine, future=True)
            statement = db.select(FuelSpecs).where(FuelSpecs.vin == arg)
            result = session.execute(statement).first()
            session.close()

            if result:
                dbFuelSpecs = result.FuelSpecs
        
        if dbFuelSpecs:
            print("Fuel tank volume: " + str(dbFuelSpecs.fuelTankVolume) + "L")
            print("Fuel type: " + str(dbFuelSpecs.fuelType))
            print("City economy: " + str(dbFuelSpecs.cityFuelEconomy) + "kpL")
            print("Highway economy: " + str(dbFuelSpecs.highwayFuelEconomy) + "kpL")
            print("")
            ret = True
    
    if info_type == "wheel" or info_type == "all":
        dbWheelSystem = None
        if arg_object:
            dbWheelSystem = arg_object
        else:
            session = Session(engine, future=True)
            statement = db.select(WheelSystem).where(WheelSystem.vin == arg)
            result = session.execute(statement).first()
            session.close()

            if result:
                dbWheelSystem = result.WheelSystem
        
        if dbWheelSystem:
            print("Drive system: " + str(dbWheelSystem.wheelSystem))
            print("Wheelbase: " + str(dbWheelSystem.wheelbase) + "cm")
            print("")
            ret = True

    if info_type == "depreciation" or info_type == "all":
        dbDepreciationFactors = None
        if arg_object:
            dbDepreciationFactors = arg_object
        else:
            session = Session(engine, future=True)
            statement = db.select(DepreciationFactors).where(DepreciationFactors.vin == arg)
            result = session.execute(statement).first()
            session.close()

            if result:
                dbDepreciationFactors = result.DepreciationFactors
        
        if dbDepreciationFactors:
            print("Damaged frame: " + str(dbDepreciationFactors.frameDamaged))
            print("Has been in an accident: " + str(dbDepreciationFactors.hasAccidents))
            print("Is salvage: " + str(dbDepreciationFactors.salvage))
            print("")
            ret = True

    return ret

# list a car for sale, given the proper relational objects
def list_car(carEngine=None, fuelSpecs=None, wheelSystem=None, trimPackage=None, depreciationFactors=None, interior=None):
    session = Session(engine)
    if carEngine is not None:
        session.add(carEngine)
    if fuelSpecs is not None:
        session.add(fuelSpecs)
    if wheelSystem is not None:
        session.add(wheelSystem)
    if trimPackage is not None:
        session.add(trimPackage)
    if depreciationFactors is not None:
        session.add(depreciationFactors)
    if interior is not None:
        session.add(interior)
    session.commit()
    session.close()

# check to see if a user already exists
def existing_user(email):
    session = Session(engine, future=True)
    statement = db.select(User).where(User.email == email)
    result = session.execute(statement).first()
    session.close()

    if result:
        return True
    return False

# construct & return a search statement using the
# filters and sorting criteria the user has selected
def build_search(page):
    statement = db.select(Car, Listing).join(Listing)

    if g_userType != 'Admin':
        statement = statement.where(Listing.activeListing == "True")

    for f in filter(active_filter, g_filters):
        column = Car
        if f['name'] == 'Year':
            column = Car.year
        elif f['name'] == 'Make':
            column = Car.franchiseMake
        elif f['name'] == 'Model':
            column = Car.modelName
        elif f['name'] == 'Price':
            column = Listing.price
        elif f['name'] == 'Color':
            column = Car.color

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
                val = "True" if f['value'] else "False"
            statement = statement.where(column == val)
        elif f['relationship'] == "!=":
            val = 0
            if f['f_type'] == "equality":
                val = f['value']
            elif f['f_type'] == "range":
                val = parse(f['value'])
            elif f['f_type'] == "boolean":
                val = "True" if f['value'] else "False"
            statement = statement.where(column != val)
        elif f['relationship'] == "<=":
            statement = statement.where(column <= parse(f['value']))
        elif f['relationship'] == "<":
            statement = statement.where(column < parse(f['value']))

    order = None
    for sort in g_sorting:
        if (sort["active"]):
            if (sort["name"] == "Price"):
                order = Listing.price
            else:
                order = Car.year

            if (sort["type"] == "standard"):
                statement = statement.order_by(db.asc(order))
            else:
                statement = statement.order_by(db.desc(order))
            break

    return statement.limit(10).offset((page - 1) * 10)

# convert a string obtained from input() into a number
# indicating the user's selection
def parse(string, allow_back=True):
    try:
        #check if string is a number for menu
        int(string)
        return int(string)
    except ValueError:
        if allow_back:
            if string == 'b':
                return 0
            elif string == 'q':
                return -1
            else:
                return -2
        return -1

# specialized input function that accepts only
# Y/y & N/n, returning boolean values
def ynput(string):
    result = 0
    while True:
        result = input(string).lower()
        if len(result) == 0 or result == "y" or result == "n":
            break
        else:
            print("Please enter only y or n.")
    return result == "y"

def list_options(options):
    print("")
    for index, option in enumerate(options):
        print(str(index + 1) + ". " + option)

# the universal function for presenting the user
# with a list of options they can select by entering
# a number
def get_input(options):
    list_options(options)
    if len(options) == 0:
        print("No options available; enter 'b' to return to the previous screen.")
    selection = parse(input("Select an option: "))
    while (selection < -1 or selection > len(options) and len(options) > 0):
        print("Invalid input.")
        list_options(options)
        selection = parse(input("Select an option: "))
    return selection

def clear_nav():
    g_loc = []

# navigate down a level
def nav_down(level):
    g_loc.append(level)
    get_loc()

# navigate up a level
def nav_up():
    g_loc.pop()
    get_loc()

# return the current location in the CLI
def get_loc():
    userType = ""
    location = "\033[1;37;40m"
    for level in g_loc:
        location += "/" + level

    if g_userType == "Admin":
        userType = "\033[1;32;40m[Admin]\033[0m | "
    elif g_userType == "Customer":
        userType = "\033[1;31;40m[Customer]\033[0m | "
    elif g_userType == "Dealer":
        userType = "\033[1;36;40m[Dealer]\033[0m | "
    elif g_userType == "DataScientist":
        userType = "\033[1;35;40m[Dealer]\033[0m | "

    location += "\033[0m"
    if len(g_loc) > 0:
        print("")
        print(userType + location)

def active_filter(f):
    return f["active"]

# main view to navigate the app
def main():
    options = []

    if g_userType != "DataScientist":
        options = ["Search Listings", "View Appointments"]
        if g_userType != "Customer":
            options.extend(["Create Listing", "View Your Listings"])
    else:
        options.extend(["DataMine"])

    nav_down("main")
    while True:
        selection = get_input(options)
        if ("Search Listings" in options and selection == options.index("Search Listings") +1):
            search()
        elif ("View Appointments" in options and selection == options.index("View Appointments") +1):
            appointments()
        elif ("Create Listing" in options and selection == options.index("Create Listing") +1):
            new_listing()
        elif ("View Your Listings" in options and selection == options.index("View Your Listings") +1):
            owned_listings()
        elif ("DataMine" in options and selection == options.index("DataMine") +1):
            dataMine()
        elif (selection == 0):
            continue
        else:
            sys.exit()

#starting point of the cli
def startup():
    print("")
    print("Welcome to Ottotradr: a used car sales platform that's definitely not affiliated with A*to Tr*der.")
    print("Navigate the application using the prompts, using 'q' to quit & 'b' to navigate back.")
    login()
    main()

# get the user to sign up or log into an account
def login():
    global g_email
    global g_userType
    global g_firstName
    options = ["Sign Up", "Log In"]
    pw1 = "1"
    pw2 = "2"
    email = "example@example.com"
    nav_down("login")

    while True:
        selection = get_input(options)
        # signup flow
        if (selection == 1):
            g_email = input("Enter your email: ")
            check_email = re.search("^\S+@\S+\.\S+$", g_email)
            exists = existing_user(g_email)
            while not check_email or exists:
                print("")
                if not check_email:
                    print("Invalid email.")
                elif exists:
                    print("Email already in use.")
                g_email = input("Enter your email: ")
                check_email = re.search("^\S+@\S+\.\S+$", g_email)
                exists = existing_user(g_email)

            userType = parse(input("Are you a Customer (1) or a Dealer (2) or a DataScientist (3): "), False)
            while userType != 1 and userType != 2 and userType != 3:
                print("")
                print("Invalid selection.")
                userType = input("Are you a Customer (1) or a Dealer (2) or a DataScientist (3): ")

            if (userType == 1):
                g_userType = "Customer"
            elif (userType == 2):
                g_userType = "Dealer"
            else:
                g_userType = "DataScientist"

            g_firstName = input("Enter your first name: ")
            g_lastname = input("Enter your last name: ")
            while (pw1 != pw2):
                password_check = False
                pw1 = input("Enter your password: (minimum 8 character, 1 uppercase, 1 lowercase, 1 number, 1 special): ")
                password_check = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", pw1)
                while (not password_check):
                    print("Invalid password format.")
                    pw1 = input("Enter your password: (minimum 8 character, 1 uppercase, 1 lowercase, 1 number, 1 special): ")
                    password_check = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", pw1)
                pw2 = input("Confirm password: ")
                if (pw1 != pw2):
                    print("Passwords do not match.")
            g_password = pw1

            print("")
            print("Email: " + g_email)
            print("Name: " + g_firstName + " " + g_lastname)
            print("Account type: " + g_userType)
            confirm = input("Type 'confirm' to create your account, or anything else to return to the login screen: ")
            if confirm.lower() != "confirm":
                continue

            g_user = User(email=g_email, firstName=g_firstName, lastName=g_lastname, password=g_password, userType=g_userType)

            session = Session(engine)
            session.add(g_user)
            session.commit()
            session.close()

            break
        # login flow
        elif (selection == 2):
            while(True):
                print("")
                f_email = input("Email: ")
                f_password = input("Password: ")

                error_because_of_bad_password = 0

                session = Session(engine, future=True)
                statement = db.select(User).where(User.email == str(f_email))
                results = session.execute(statement).first()
                session.close()

                if (results):
                    if (f_password != results.User.password):
                        print("Incorrect password.")
                        continue
                    else:
                        g_userType = results.User.userType
                        g_email = results.User.email
                        g_firstName = results.User.firstName
                        break
                else:
                    print("User not found.")
                    continue
            break
            
        elif (selection == 0):
            continue
        elif (selection == -1):
            sys.exit()
    
    print("Login successful! Welcome to Ottotradr,", g_firstName)

    nav_up()

# create a new appointment, prompting the user for input
def new_appointment(l_id):
    nav_down("new_appointment")

    session = Session(engine, future=True)
    statement = db.select(Listing, User, Car).join(User, Listing.dealerEmail == User.email).join(Car).where(Listing.listingId == l_id)
    result = session.execute(statement).first()
    session.close()

    dealerEmail = result.Listing.dealerEmail

    print("You're setting up a meeting with {name:s} regarding the purchase of a {car:s}.".format(name=str(result.User.firstName) + " " + str(result.User.lastName), car=str(result.Car.franchiseMake) + " " + str(result.Car.modelName)))
    print("Please fill out the below information.")

    appointmentDateTime = 0
    information = ""

    while True:
        appointmentDateTime = input("When would you like to schedule the appointment for (DDMMYYYY): ")
        try:
            int(appointmentDateTime)
            if (len(appointmentDateTime) != 8):
                print("Please enter a valid date.")
                continue
            break
        except ValueError:
            print("Please enter a valid date.")
            continue

    while True:
        hour = 0
        minute = 0
        appointmentTime = input("When would you like to schedule the appointment for (HH:MM, 24hr): ")
        try:
            hour = int(appointmentTime[0:2])
            minute = int(appointmentTime[3:5])
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                print("Please enter a valid time.")
                continue
        except ValueError:
            print("Please enter a valid time.")
            continue

        appointmentDateTime = datetime.datetime(
            int(appointmentDateTime[4:8]),
            int(appointmentDateTime[2:4]),
            int(appointmentDateTime[0:2]),
            hour,
            minute
        )
        break

    information = input("Please enter any extra information you'd like to attach to the appointment: ")

    session = Session(engine, future=True)
    statement = db.select(Appointment).where(Appointment.dealerEmail == dealerEmail).where(Appointment.customerEmail == g_email)
    results = session.execute(statement).all()
    session.close()

    appointmentNumber = len(results)

    appointment = Appointment(
        appointmentNumber=format_for_db(appointmentNumber, "integer"),
        dealerEmail=format_for_db(dealerEmail, "string", 125),
        customerEmail=format_for_db(g_email, "string", 125),
        appointmentDateTime=appointmentDateTime,
        information=format_for_db(information, "string", 400),
        active=format_for_db(True, "boolean"),
        listingId=format_for_db(l_id, "integer")
    )

    session = Session(engine)
    session.add(appointment)
    session.commit()
    session.close()

    print("Your appointment has been successfully created.")
            
    nav_up()

# display the user's appointments in truncated form, with the option
# to display them in long form/access edit & cancel functionality
def appointments():
    nav_down("appointments")

    while True:

        print("")
        sys.stdout.write("\rRetrieving appointments (this may take some time)...")

        dealer = aliased(User)
        customer = aliased(User)

        session = Session(engine, future=True)
        statement = 0

        if (g_userType == "Dealer"):
            statement = db.select(Appointment, User).join(User, Appointment.customerEmail == User.email).where(Appointment.dealerEmail == g_email)
        elif (g_userType == "Customer"):
            statement = db.select(Appointment, User).join(User, Appointment.dealerEmail == User.email).where(Appointment.customerEmail == g_email)
        else:
            statement = db.select(Appointment, dealer, customer).join(dealer, Appointment.dealerEmail == dealer.email).join(customer, Appointment.customerEmail == customer.email)
        
        if (g_userType != "Admin"):
            statement = statement.where(Appointment.active == "True")

        results = session.execute(statement).all()
        session.close()

        if (len(results) == 0):
            sys.stdout.write("\rLooks like you don't have any appointments! You can create them from the detail view of a listing.")
            sys.stdout.flush()
            print("")
            break
        else:
            sys.stdout.write("\rYou can see your appointments below; select one to view it in more detail, edit, or delete it.")
            sys.stdout.flush()
            print("")
            options = []
            option_ids = []

            if (g_userType != "Admin"):
                for appointment, user in results:
                    option_ids.append([appointment.appointmentNumber, appointment.dealerEmail, appointment.customerEmail])
                    options.append("Appointment with {name:s} on {date:s} at {time:s}".format(
                                                                                        name=user.firstName + " " + user.lastName,
                                                                                        date=appointment.appointmentDateTime.strftime("%x"),
                                                                                        time=appointment.appointmentDateTime.strftime("%X")
                                                                                    ))
            else:
                for appointment, dealer, customer in results:
                    option_ids.append([appointment.appointmentNumber, appointment.dealerEmail, appointment.customerEmail])
                    options.append("Appointment between {dealerName:s} (Dealer) and {customerName:s} (Customer) on {date:s} at {time:s}".format(
                                                                                                                                            dealerName=dealer.firstName + " " + dealer.lastName,
                                                                                                                                            customerName=customer.firstName + " " + customer.lastName,
                                                                                                                                            date=appointment.appointmentDateTime.strftime("%x"),
                                                                                                                                            time=appointment.appointmentDateTime.strftime("%X")
                                                                                                                                        ))

            selection = get_input(options)
            if (selection > 0 and selection <= len(options)):
                appointment_detail(option_ids[selection - 1][0], option_ids[selection - 1][1], option_ids[selection - 1][2])
            elif (selection == 0):
                break
            elif (selection == -1):
                sys.exit()

    nav_up()

# detail view of the appointment, where the user can
# edit or cancel an appointment
def appointment_detail(aptNum, dealerEmail, userEmail):
    nav_down("appointment_detail")

    while True:
        dealer = aliased(User)
        customer = aliased(User)

        session = Session(engine, future=True)
        statement = 0

        if (g_userType == "Customer"):
            statement = db.select(Appointment, User).join(User, Appointment.dealerEmail == User.email)
        elif (g_userType == "Dealer"):
            statement = db.select(Appointment, User).join(User, Appointment.customerEmail == User.email)
        else:
            statement = db.select(Appointment, dealer, customer).join(dealer, Appointment.dealerEmail == dealer.email).join(customer, Appointment.customerEmail == customer.email)

        statement = statement.where(Appointment.appointmentNumber == aptNum).where(Appointment.dealerEmail == dealerEmail).where(Appointment.customerEmail == userEmail).where(Appointment.active == "True")
        result = session.execute(statement).one()
        session.close()

        if (g_userType == "Customer"):
            print("Dealer: " + result.User.firstName + " " + result.User.lastName)
            print("Dealer email: " + result.Appointment.dealerEmail)
        elif (g_userType == "Dealer"):
            print("Customer: " + result.User.firstName + " " + result.User.lastName)
            print("Customer email: " + result.Appointment.customerEmail)
        else:
            print("Dealer: " + result[1].firstName + " " + result[1].lastName)
            print("Dealer email: " + result[0].dealerEmail)
            print("Customer: " + result[2].firstName + " " + result[2].lastName)
            print("Customer email: " + result[0].customerEmail)
        print("Appointment date & time: " + result.Appointment.appointmentDateTime.strftime("%c"))
        print("Extra information: " + str(result.Appointment.information))
        
        options = ["Edit Appointment", "Cancel Appointment"]
        selection = get_input(options)
        if selection > 0 and selection <= len(options):
            if selection == 1:
                edit_appointment(aptNum, dealerEmail, userEmail)
            else:
                remove_appointment(aptNum, dealerEmail, userEmail)
                print("Appointment cancelled.")
                break
        elif selection == 0:
            break
        else:
            sys.exit()

    nav_up()

# edit an appointment by selecting the specific
# fields the user would like to modify
def edit_appointment(aptNum, dealerEmail, userEmail):
    nav_down("edit_appointment")

    dealer = aliased(User)
    customer = aliased(User)

    session = Session(engine, future=True)
    statement = 0

    if (g_userType == "Customer"):
        statement = db.select(Appointment, User).join(User, Appointment.dealerEmail == User.email)
    elif (g_userType == "Dealer"):
        statement = db.select(Appointment, User).join(User, Appointment.customerEmail == User.email)
    else:
        statement = db.select(Appointment, dealer, customer).join(dealer, Appointment.dealerEmail == dealer.email).join(customer, Appointment.customerEmail == customer.email)

    statement = statement.where(Appointment.appointmentNumber == aptNum and Appointment.dealerEmail == dealerEmail and Appointment.userEmail == userEmail)
    result = session.execute(statement).first()
    session.close()

    appointmentDateTime = result.Appointment.appointmentDateTime
    information = result.Appointment.information

    while True:
        print("Appointment date & time: " + appointmentDateTime.strftime("%c"))
        if (information):
            print("Extra information: " + information)

        options = ["Date & Time", "Information", "Save & Go Back"]
        selection = get_input(options)
        if selection > 0 and selection < len(options):
            if selection == 1:
                while True:
                    hour = 0
                    minute = 0
                    appointmentTime = input("When would you like to schedule the appointment for (HH:MM, 24hr): ")
                    try:
                        hour = int(appointmentTime[0:2])
                        minute = int(appointmentTime[3:5])
                        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                            print("Please enter a valid time (HH:MM, 24hr).")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid time (HH:M, 24hr).")
                        continue

                while True:
                    appointmentDate = input("When would you like to schedule the appointment for (DDMMYYYY): ")
                    try:
                        int(appointmentDate)
                        if (len(appointmentDate) != 8):
                            print("Please enter a valid date (DDMMYYYY).")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid date (DDMMYYYY).")
                        continue

                appointmentDateTime = datetime.datetime(
                    int(appointmentDate[4:8]),
                    int(appointmentDate[2:4]),
                    int(appointmentDate[0:2]),
                    hour,
                    minute
                )
            else:
                information = input("Please enter any extra information you'd like to attach to the appointment: ")
        elif selection == len(options):
            session = Session(engine)
            statement = session.query(Appointment).filter(
                Appointment.appointmentNumber == aptNum
            ).filter(
                Appointment.dealerEmail == dealerEmail
            ).filter(
                Appointment.customerEmail == userEmail
            ).update({
                "information": format_for_db(information, "string", 1000),
                "appointmentDateTime": appointmentDateTime
            })
            session.commit()
            session.close()
            print("Appointment updated.")
            break
        elif selection == 0:
            break
        elif selection == -1:
            sys.exit()

    nav_up()

# cancel an appointment by setting its active property to False
def remove_appointment(aptNum, dealerEmail, userEmail):
    session = Session(engine)
    session.query(Appointment).filter(
            Appointment.appointmentNumber == aptNum
        ).filter(
            Appointment.dealerEmail == dealerEmail
        ).filter(
            Appointment.customerEmail == userEmail
        ).update({"active":"False"})
    session.commit()
    session.close()

# display a user's listings in truncated form,
# with the option to view a listing in long form
# and edit/delete a listing (also by setting its active field)
def owned_listings():
    nav_down("owned_listings")

    page = 1

    while True:
        print("")
        sys.stdout.write("\rRetrieving owned listings (this may take some time)...")
        session = Session(engine, future=True)
        statement = db.select(Car, Listing).join(Listing).where(Listing.dealerEmail == str(g_email))
        if g_userType != "Admin":
            statement = statement.where(Listing.activeListing == "True")
        statement = statement.limit(10).offset((page - 1) * 10)
        results = session.execute(statement).all()
        session.close()

        if (len(results) == 0):
            sys.stdout.write("\rLooks like you don't have any listings! You can create them from the main page.")
            sys.stdout.flush()
            print("")
            break
        else:
            sys.stdout.write("\rYou can see your listings below; select one to view it in more detail, edit, or remove it.")
            sys.stdout.flush()
            print("")
            options = []
            option_ids = []
            for car, listing in results:
                option_ids.append(car.listingId)
                options.append(car.franchiseMake + " " + car.modelName + " [$" + str(listing.price) + "]")
            options.extend(["Previous Page", "Next Page"])
            selection = get_input(options)
            if (selection > 0 and selection <= len(options) - 2):
                detail(option_ids[selection - 1])
            elif selection == len(options) - 1:
                if page > 1:
                    page -= 1
            elif selection == len(options):
                if len(results) == 10:
                    page += 1
            elif (selection == 0):
                break
            else:
                sys.exit()

    nav_up()

# take the user through the process to create
# a new listing with engine, interior, etc 
# being optional
def new_listing():
    nav_down("new_listing")
    print("")
    is_valid_vin = False
    vin = 0

    while True:
        vin = input("Enter vehicle VIN number: ")
        if ( vin.isnumeric() and len(vin) >= 11 and len(vin) <= 17 ):
            break
    
    make = input("Enter vehicle make: ")
    model = input("Enter vehicle model: ")
    height = input("Enter vehicle height (cm): ")
    width = input("Enter vehicle width (cm): ")
    length = input("Enter vehicle length (cm): ")
    color = input("Enter vehicle color: ")
    bodyType = input("Enter vehicle body type: ")
    year = input("Enter vehicle year of make: ")
    price = input("Enter desired list price: ")
    isCab = ynput("Was this vehicle a cab (y/n): ")
    trimPackageID = input("Enter vehicle trim package identifier: ")

    listing = None
    wheelSystem = None
    carEngine = None
    interior = None
    trimPackage = None
    fuelSpecs = None
    depreciationFactors = None
    
    hasEngine = ynput("Do you know the engine specifications of the vehicle (y/n): ")
    if hasEngine:
        print("If you don't know the answer to any field, or it isn't applicable, leave it blank.")
        displacement = input("Enter engine displacement (ml): ")
        engineType = input("Enter engine type: ")
        cylinders = input("Enter number of cylinders: ")
        horsepower = input("Enter engine horsepower: ")
        transmission = input("Enter engine transmission: ")
        carEngine = Engine(
            vin=format_for_db(vin, "string", 17),
            engineCylinders=format_for_db(cylinders, "string", 40),
            engineDisplacement=format_for_db(displacement, "float", 8, 3),
            engineType=format_for_db(engineType, "string", 40),
            horsepower=format_for_db(horsepower, "float", 5, 2),
            transmission=format_for_db(transmission, "string", 40)
        )
    print("")
    
    hasInterior = ynput("Do you know the interior specifications of the vehicle (y/n): ")
    if hasInterior:
        print("If you don't know the answer to any field, or it isn't applicable, leave it blank.")
        frontLegroom = input("Enter front legroom (cm): ")
        backLegroom = input("Enter rear legroom (cm): ")
        maximumSeating = input("Enter maximum seating capacity: ")
        interiorColor = input("Enter interior color: ")
        interior = Interior(
            vin=format_for_db(vin, "string", 17),
            frontLegroom=format_for_db(frontLegroom, "float", 4, 1),
            backLegroom=format_for_db(backLegroom, "float", 4, 1),
            interiorColor=format_for_db(interiorColor, "string", 125),
            maximumSeating=format_for_db(maximumSeating, "integer")
        )
    print("")
    
    hasFuel = ynput("Do you know the fuel specifications of the vehicle (y/n): ")
    if hasFuel:
        print("If you don't know the answer to any field, or it isn't applicable, leave it blank.")
        fuelTankVolume = input("Enter fuel tank volume (l): ")
        fuelType = input("Enter fuel type: ")
        cityFuelEconomy = input("Enter city fuel economy (kpl): ")
        highwayFuelEconomy = input("Enter highway fuel economy (kpl): ")
        fuelSpecs = FuelSpecs(
            vin=format_for_db(vin, "string", 17),
            fuelTankVolume=format_for_db(fuelTankVolume, "float", 4, 1),
            fuelType=format_for_db(fuelType, "string", 40),
            cityFuelEconomy=format_for_db(cityFuelEconomy, "float", 5, 2),
            highwayFuelEconomy=format_for_db(highwayFuelEconomy, "float", 5, 2)
        )
    print("")

    hasWheelbase = ynput("Do you know the wheelbase specifications of the vehicle (y/n): ")
    if hasWheelbase:
        print("If you don't know the answer to any field, or it isn't applicable, leave it blank.")
        wheelSystemDesc = input("Enter vehicle wheel system (3 letter designation): ")
        wheelbase = input("Enter vehicle wheelbase width (cm): ")
        wheelSystem = WheelSystem(
            vin=format_for_db(vin, "string", 17),
            wheelSystem=format_for_db(wheelSystemDesc, "string", 3),
            wheelbase=format_for_db(wheelbase, "float", 4, 1)
        )
    print("")
    
    frameDamaged = ynput("Is the vehicle's frame damaged (y/n): ")
    hasAccidents = ynput("Has this vehicle been involved in any accidents (y/n): ")
    salvage = ynput("Is this vehicle salvage (y/n): ")
    depreciationFactors = DepreciationFactors(
        vin=format_for_db(vin, "string", 17),
        frameDamaged=format_for_db(frameDamaged, "boolean"),
        hasAccidents=format_for_db(hasAccidents, "boolean"),
        salvage=format_for_db(salvage, "boolean")
    )
    print("")

    if len(trimPackageID) > 0:
        trimPackage = TrimPackage(
            vin=format_for_db(vin, "string", 17),
            trimName=format_for_db(trimPackageID, "string", 125)
        )

    print("You are about to list the following vehicle for sale:")
    print("VIN: " + vin)
    print("Make: " + make)
    print("Model: " + model)
    print("Body type: " + bodyType)
    print("Year: " + year)
    print("Price: $" + price)
    print("Cab: " + ("True" if isCab else "False"))
    if trimPackage is not None:
        print_listing("trim", arg_object=trimPackage)
    if hasEngine:
        print_listing("engine", arg_object=carEngine)
    if hasInterior:
        print_listing("interior", arg_object=interior)
    if hasFuel:
        print_listing("fuel", arg_object=fuelSpecs)
    if hasWheelbase:
        print_listing("wheel", arg_object=wheelSystem)
    
    print_listing("depreciation", arg_object=depreciationFactors)

    print("")

    listingDescription = input("Enter a description for this listing: ")

    listing = Listing(
        listingDate=datetime.date.today(),
        daysOnMarket=0,
        description=format_for_db(listingDescription, "string", 1000),
        price=format_for_db(price, "float", 9, 2),
        dealerEmail=format_for_db(g_email, "string", 125),
        activeListing=format_for_db(True, "boolean")
    )

    confirm = input("Please type 'confirm' to list this vehicle, or any other input to cancel: ")

    if (confirm == "confirm"):
        session = Session(engine)
        session.add(listing)
        session.commit()

        car = Car(
            vin=format_for_db(vin, "string", 17),
            bodyType=format_for_db(bodyType, "string", 40),
            height=format_for_db(height, "float", 4, 1),
            length=format_for_db(length, "float", 4, 1),
            width=format_for_db(width, "float", 4, 1),
            color=format_for_db(color, "string", 125),
            year=format_for_db(year, "integer"),
            modelName=format_for_db(model, "string", 40),
            franchiseMake=format_for_db(make, "string", 40),
            isCab=format_for_db(isCab, "boolean"),
            listingId=format_for_db(listing.listingId, "integer")
        )

        session.add(car)
        session.commit()
        session.close()

        list_car(
            trimPackage=trimPackage,
            carEngine=carEngine,
            interior=interior,
            wheelSystem=wheelSystem,
            fuelSpecs=fuelSpecs,
            depreciationFactors=depreciationFactors
        )
        print("Car listed for sale!")
    else:
        print("Listing cancelled.")
    
    nav_up()

# main search view, from which users can add, remove, and edit filters, 
# as well as sorting and actually displaying results
def search():
    nav_down("search")
    options = ["Add Filters", "View & Remove Filters", "Sort Results", "Display Results"]
    while True:
        selection = get_input(options)
        if (selection == 1):
            addfilters()
        elif (selection == 2):
            removefilters()
        elif (selection == 3):
            selectsort()
        elif (selection == 4):
            display()
        elif (selection == 0):
            break
        else:
            sys.exit()

    nav_up()

# display the results of a search, using the
# build_search feature to assemble the SQL statement
# based on the active filters & sort criteria
def display():
    nav_down("search_results")

    page = 1

    while True:
        print("")
        sys.stdout.write("\rSearching (this may take some time)...")

        options = []
        option_ids = []
        session = Session(engine, future=True)
        statement = build_search(page)
        result = session.execute(statement).all()
        session.close()

        if page > 1 and len(result) == 0:
            page -= 1
            continue

        sys.stdout.write("\rSelect a listing to view it in detail. [Page {page:d}]\n".format(page=page))
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
            sys.exit()

# view a listing in long form & make an appointment (customer)
# or edit/remove it (dealer who owns the listing)
def detail(l_id):
    nav_down("listing_detail")
    
    session = Session(engine, future=True)
    statement = db.select(Listing).where(Listing.listingId == l_id)
    result = session.execute(statement).first()
    session.close()

    print_listing("all", l_id)
    options = []

    owned = False
    admin = False

    while True:
        if (g_userType == "Dealer"):
            if result.Listing.dealerEmail == g_email:
                options = ["Edit Listing", "Remove Listing", "Show Listing Details"]
                owned = True
        elif (g_userType == "Customer"):
            options = ["Make An Appointment", "Show Listing Details"]
        else:
            options = ["Make An Appointment", "Edit Listing", "Remove Listing", "Show Listing Details"]
            admin = True
        selection = get_input(options)
        if owned and not admin:
            if (selection == 1):
                editlisting(l_id)
            elif (selection == 2):
                removelisting(l_id)
                nav_up()
                return
            elif selection == 3:
                print_listing("all", l_id)
            elif (selection == 0):
                nav_up()
                return
            elif (selection == -1):
                sys.exit()
        elif not admin:
            if selection == 1:
                new_appointment(result.Listing.listingId)
                nav_up()
                return
            elif selection == 2:
                print_listing("all", l_id)
            elif selection == 0:
                nav_up()
                return
            else:
                sys.exit()
        else:
            if selection == 1:
                new_appointment(result.Listing.listingId)
                break
            elif selection == 2:
                editlisting(l_id)
            elif selection == 3:
                removelisting(l_id)
                break
            elif selection == 4:
                print_listing("all", l_id)
            elif selection == 0:
                break
            else:
                sys.exit()

    nav_up()
    
# remove a listing by setting its active property to False
def removelisting(l_id):
    nav_down("remove_listing")
    print("")
    
    session = Session(engine, future=True)
    statement = db.select(Car).join(Listing).where(Listing.listingId == l_id)
    result = session.execute(statement).first()
    session.close()
    print("VIN: " + result.Car.vin)
    confirm = input("Enter this vehicle's VIN to confirm listing deletion: ")
    if (confirm == result.Car.vin):
        session = Session(engine)
        session.query(Listing).filter(Listing.listingId == l_id).update({"activeListing":"False"})
        session.commit()
        session.close()
        print("Listing removed.")
    else:
        print("Listing not removed.")

    nav_up()

# Top level view for editing a listing
def editlisting(l_id):
    nav_down("edit_listing")
    
    session = Session(engine, future=True)
    statement = db.select(Car, Listing).join(Listing).where(Car.listingId == l_id)
    result = session.execute(statement).first()
    session.close()

    vin = result.Car.vin
    
    while True:
        options = ["Basic Options", "Engine", "Trim", "Interior", "Fuel", "Wheel System", "Depreciation Factors"]
        selection = get_input(options)
        if selection == 1:
            edit_basic(l_id)
        elif selection == 2:
            edit_engine(vin)
        elif selection == 3:
            edit_trim(vin)
        elif selection == 4:
            edit_interior(vin)
        elif selection == 5:
            edit_fuel(vin)
        elif selection == 6:
            edit_wheelbase(vin)
        elif selection == 7:
            edit_depreciation(vin)
        elif selection == 0:
            break
        elif selection == -1:
            sys.exit()

    nav_up()

# Edit the Car and Listing relations
def edit_basic(l_id):
    nav_down("edit_basic")

    session = Session(engine)
    statement = db.select(Car, Listing).join(Listing).where(Listing.listingId == l_id)
    result = session.execute(statement).first()
    session.close()
    
    car = None
    listing = None

    if result:
        car = result.Car
        listing = result.Listing

    while True:
        if listing and car:
            options = ["Body Type", "Height", "Year", "Model", "Make", "New", "Cab", "Price", "Width", "Length", "Color", "Description", "View Basic Information", "Save & Go Back"]
            selection = get_input(options)
            if selection > 0 and selection < len(options) - 1:
                if selection == 1:
                    value = input("Enter body type: ")
                    car.bodyType = format_for_db(value, "string", 40)
                elif selection == 2:
                    value = input("Enter height: ")
                    car.height = format_for_db(value, "float", 4, 1)
                elif selection == 3:
                    value = input("Enter year: ")
                    car.year = format_for_db(value, "integer")
                elif selection == 4:
                    value = input("Enter model: ")
                    car.modelName = format_for_db(value, "string", 40)
                elif selection == 5:
                    value = input("Enter make: ")
                    car.franchiseMake = format_for_db(value, "string", 40)
                elif selection == 6:
                    value = input("Was this vehicle a cab (y/n): ")
                    car.isCab = format_for_db(value, "boolean")
                elif selection == 7:
                    value = input("Enter desired list price: ")
                    listing.price = format_for_db(value, "float", 9, 2)
                elif selection == 8:
                    value = input("Enter width: ")
                    car.width = format_for_db(value, "float", 4, 1)
                elif selection == 9:
                    value = input("Enter lenght: ")
                    car.length = format_for_db(value, "float", 4, 1)
                elif selection == 10:
                    value = input("Enter color: ")
                    car.color = format_for_db(value, "string", 125)
                else:
                    value = input("Enter listing description: ")
                    listing.description = format_for_db(value, "string", 1000)
            elif selection == len(options) - 1:
                print_listing("listing", arg_object=listing)
                print_listing("car", arg_object=car)
            elif selection == len(options):
                session = Session(engine)
                session.query(Listing).filter(Listing.listingId == listing.listingId).update({
                    "price": listing.price,
                    "description": listing.description
                })
                session.query(Car).filter(Car.vin == car.vin).update({
                    "bodyType": car.bodyType,
                    "height": car.height,
                    "width": car.width,
                    "length": car.length,
                    "color": car.color,
                    "year": car.year,
                    "modelName": car.modelName,
                    "franchiseMake": car.franchiseMake,
                    "isCab": car.isCab,
                })
                session.commit()
                session.close()
                print("")
                print("Basic information saved.")
                break
            elif selection == 0:
                break
            else:
                sys.exit()
        else:
            print("If you're seeing this, this application is really broken. My bad, hope there isn't a prof or a TA reading this!")
            break

    nav_up()

# Edit the trim relation, or add one if it doesn't exist
def edit_trim(vin):
    nav_down("edit_trim")

    session = Session(engine)
    statement = db.select(TrimPackage).where(TrimPackage.vin == vin)
    result = session.execute(statement).first()
    session.close()
    
    trimPackage = None

    if result:
        trimPackage = result.TrimPackage

    while True:
        if trimPackage:
            options = ["Trim Name", "View Trim Package", "Save & Go Back"]
            selection = get_input(options)
            if selection > 0 and selection < len(options) - 1:
                if selection == 1:
                    trimName = input("Enter trim name: ")
                    trimPackage.trimName = format_for_db(trimName, "string", 125)
            elif selection == len(options) - 1:
                print_listing("trim", arg_object=trimPackage)
            elif selection == len(options):
                session = Session(engine)
                session.query(TrimPackage).filter(TrimPackage.vin == vin).update({"trimName": trimPackage.trimName})
                session.commit()
                session.close()
                print("")
                print("Trim package saved.")
                break
            elif selection == 0:
                break
            else:
                sys.exit()
        else:
            new_trim = ynput("Trim package not found. Would you like to add one (y/n)?: ")
            if new_trim:
                print("")
                trimName = input("Enter vehicle trim package identifier: ")
                trimPackage = TrimPackage(
                    vin=format_for_db(vin, "string", 17),
                    trimName=format_for_db(trimName, "string", 125)
                )
                session = Session(engine)
                session.add(trimPackage)
                session.commit()
                session.close()
                print("Trim package added!")
                break
            else:
                break

    nav_up()

# Edit the engine relation, or add one if it doesn't exist
def edit_engine(vin):
    nav_down("edit_engine")

    session = Session(engine, future=True)
    statement = db.select(Engine).where(Engine.vin == vin)
    result = session.execute(statement).first()
    session.close()

    carEngine = None

    if result:
        carEngine = result.Engine

    while True:
        if carEngine:
            options = ["Engine Cylinders", "Engine Displacement", "Engine Type", "Horsepower", "Transmission", "View Engine", "Save & Go Back"]
            selection = get_input(options)
            if selection > 0 and selection < len(options) - 1:
                if selection == 1:
                    value = input("Enter cylinders: ")
                    carEngine.engineCylinders = format_for_db(value, "string", 40)
                elif selection == 2:
                    value = input("Enter displacement: ")
                    carEngine.engineDisplacement = format_for_db(value, "float", 8, 3)
                elif selection == 3:
                    value = input("Enter engine type: ")
                    carEngine.engineType = format_for_db(value, "string", 40)
                elif selection == 4:
                    value = input("Enter horsepower: ")
                    carEngine.horsepower = format_for_db(value, "float", 5, 2)
                else:
                    value = input("Enter transmission type: ")
                    carEngine.transmission = format_for_db(value, "string", 40)
            elif selection == len(options) - 1:
                print_listing("engine", arg_object=carEngine)
            elif selection == len(options):
                session = Session(engine)
                session.query(Engine).filter(Engine.vin == vin).update({
                    "engineCylinders": carEngine.engineCylinders,
                    "engineDisplacement": carEngine.engineDisplacement,
                    "engineType": carEngine.engineType,
                    "horsepower": carEngine.horsepower,
                    "transmission": carEngine.transmission
                })
                session.commit()
                session.close()
                print("")
                print("Engine information saved.")
                break
            elif selection == 0:
                break
            else:
                sys.exit()
        else:
            new_engine = ynput("Engine information not found. Would you like to add it (y/n)?: ")
            if new_engine:
                print("")
                print("If you don't know the answer to any field, or it isn't applicable, leave it blank.")
                displacement = input("Enter engine displacement (ml): ")
                engineType = input("Enter engine type: ")
                cylinders = input("Enter number of cylinders: ")
                horsepower = input("Enter engine horsepower: ")
                transmission = input("Enter engine transmission: ")
                carEngine = Engine(
                    vin=format_for_db(vin, "string", 17),
                    engineCylinders=format_for_db(cylinders, "string", 40),
                    engineDisplacement=format_for_db(displacement, "float", 8, 3),
                    engineType=format_for_db(engineType, "string", 40),
                    horsepower=format_for_db(horsepower, "float", 5, 2),
                    transmission=format_for_db(transmission, "string", 40)
                )
                session = Session(engine)
                session.add(carEngine)
                session.commit()
                session.close()
                print("Engine information added!")
                break
            else:
                break

    nav_up()

# Edit the interior relation, or add one if it doesn't exist
def edit_interior(vin):
    nav_down("edit_interior")

    session = Session(engine, future=True)
    statement = db.select(Interior).where(Interior.vin == vin)
    result = session.execute(statement).first()
    session.close()

    interior = None

    if result:
        interior = result.Interior

    while True:
        if interior:
            options = ["Back Legroom", "Front Legroom", "Interior Color", "Maximum Seating", "View Interior", "Save & Go Back"]
            selection = get_input(options)
            if selection > 0 and selection < len(options) - 1:
                if selection == 1:
                    value = input("Enter back legroom: ")
                    interior.backLegroom = format_for_db(value, "float", 4, 1)
                elif selection == 2:
                    value = input("Enter front legroom: ")
                    interior.frontLegroom = format_for_db(value, "float", 4, 1)
                elif selection == 3:
                    value = input("Enter interior color: ")
                    interior.interiorColor = format_for_db(value, "string", 125)
                else:
                    value = input("Enter maximum seating: ")
                    interior.maximumSeating = format_for_db(value, "integer")
            elif selection == len(options) - 1:
                print_listing("interior", arg_object=interior)
            elif selection == len(options):
                session = Session(engine)
                session.query(Interior).filter(Interior.vin == vin).update({
                    "backLegroom": interior.backLegroom,
                    "frontLegroom": interior.frontLegroom,
                    "interiorColor": interior.interiorColor,
                    "maximumSeating": interior.maximumSeating
                })
                session.commit()
                session.close()
                print("")
                print("Interior information saved.")
                break
            elif selection == 0:
                break
            else:
                sys.exit()
        else:
            new_interior = ynput("Interior information not found. Would you like to add it (y/n)?: ")
            if new_interior:
                print("")
                print("If you don't know the answer to any field, or it isn't applicable, leave it blank.")
                frontLegroom = input("Enter front legroom (cm): ")
                backLegroom = input("Enter rear legroom (cm): ")
                maximumSeating = input("Enter maximum seating capacity: ")
                interiorColor = input("Enter interior color: ")
                interior = Interior(
                    vin=format_for_db(vin, "string", 17),
                    frontLegroom=format_for_db(frontLegroom, "float", 4, 1),
                    backLegroom=format_for_db(backLegroom, "float", 4, 1),
                    interiorColor=format_for_db(interiorColor, "string", 125),
                    maximumSeating=format_for_db(maximumSeating, "integer")
                )
                session = Session(engine)
                session.add(interior)
                session.commit()
                session.close()
                print("Interior information added!")
                break
            else:
                break

    nav_up()

# Edit the fuel relation, or add one if it doesn't exist
def edit_fuel(vin):
    nav_down("edit_fuel")

    session = Session(engine, future=True)
    statement = db.select(FuelSpecs).where(FuelSpecs.vin == vin)
    result = session.execute(statement).first()
    session.close()

    fuelSpecs = None

    if result:
        fuelSpecs = result.FuelSpecs

    while True:
        if fuelSpecs:
            options = ["Fuel Tank Volume", "Fuel Type", "Highway Fuel Economy", "City Fuel Economy", "View Fuel Specs", "Save & Go Back"]
            selection = get_input(options)
            if selection > 0 and selection < len(options) - 1:
                if selection == 1:
                    value = input("Enter fuel tank volume (L): ")
                    fuelSpecs.fuelTankVolume = format_for_db(value, "float", 4, 1)
                elif selection == 2:
                    value = input("Enter fuel type: ")
                    fuelSpecs.fuelType = format_for_db(value, "string", 40)
                elif selection == 3:
                    value = input("Enter highway fuel economy (mpl): ")
                    fuelSpecs.highwayFuelEconomy = format_for_db(value, "float", 5, 2)
                else:
                    value = input("Enter city fuel economy (mpl): ")
                    fuelSpecs.cityFuelEconomy = format_for_db(value, "float", 5, 2)
            elif selection == len(options) - 1:
                print_listing("fuel", arg_object=fuelSpecs)
            elif selection == len(options):
                session = Session(engine)
                session.query(FuelSpecs).filter(FuelSpecs.vin == vin).update({
                    "fuelTankVolume": fuelSpecs.fuelTankVolume,
                    "fuelType": fuelSpecs.fuelType,
                    "highwayFuelEconomy": fuelSpecs.highwayFuelEconomy,
                    "cityFuelEconomy": fuelSpecs.cityFuelEconomy
                })
                session.commit()
                session.close()
                print("")
                print("Fuel specifications saved.")
                break
            elif selection == 0:
                break
            else:
                sys.exit()
        else:
            new_interior = ynput("Fuel specifications not found. Would you like to add them (y/n)?: ")
            if new_interior:
                print("")
                print("If you don't know the answer to any field, or it isn't applicable, leave it blank.")
                fuelTankVolume = input("Enter fuel tank volume (l): ")
                fuelType = input("Enter fuel type: ")
                cityFuelEconomy = input("Enter city fuel economy (kpl): ")
                highwayFuelEconomy = input("Enter highway fuel economy (kpl): ")
                fuelSpecs = FuelSpecs(
                    vin=format_for_db(vin, "string", 17),
                    fuelTankVolume=format_for_db(fuelTankVolume, "float", 4, 1),
                    fuelType=format_for_db(fuelType, "string", 40),
                    cityFuelEconomy=format_for_db(cityFuelEconomy, "float", 5, 2),
                    highwayFuelEconomy=format_for_db(highwayFuelEconomy, "float", 5, 2)
                )
                session = Session(engine)
                session.add(fuelSpecs)
                session.commit()
                session.close()
                print("Fuel specifications added!")
                break
            else:
                break

    nav_up()

# Edit the wheelbase relation, or add one if it doesn't exist
def edit_wheelbase(vin):
    nav_down("edit_wheelbase")

    session = Session(engine, future=True)
    statement = db.select(WheelSystem).where(WheelSystem.vin == vin)
    result = session.execute(statement).first()
    session.close()

    wheelSystem = None

    if result:
        wheelSystem = result.WheelSystem

    while True:
        if fuelSpecs:
            options = ["Wheel System Designation", "Wheelbase", "View Wheel System", "Save & Go Back"]
            selection = get_input(options)
            if selection > 0 and selection < len(options) - 1:
                if selection == 1:
                    value = input("Enter wheel system designation (3 letter acronym): ")
                    wheelSystem.wheelSystem = format_for_db(value, "string", 3)
                else:
                    value = input("Enter wheelbase width (cm): ")
                    wheelSystem.wheelbase = format_for_db(value, "float", 4, 1)
            elif selection == len(options) - 1:
                print_listing("wheel", arg_object=wheelSystem)
            elif selection == len(options):
                session = Session(engine)
                session.query(FuelSpecs).filter(FuelSpecs.vin == vin).update({
                    "wheelSystem": wheelSystem.wheelSystem,
                    "wheelbase": wheelSystem.wheelbase
                })
                session.commit()
                session.close()
                print("")
                print("Wheel system saved.")
                break
            elif selection == 0:
                break
            else:
                sys.exit()
        else:
            new_interior = ynput("Wheel system not found. Would you like to add one (y/n)?: ")
            if new_interior:
                print("")
                print("If you don't know the answer to any field, or it isn't applicable, leave it blank.")
                wheelSystemDesc = input("Enter vehicle wheel system (3 letter designation): ")
                wheelbase = input("Enter vehicle wheelbase width (cm): ")
                wheelSystem = WheelSystem(
                    vin=format_for_db(vin, "string", 17),
                    wheelSystem=format_for_db(wheelSystemDesc, "string", 3),
                    wheelbase=format_for_db(wheelbase, "float", 4, 1)
                )
                session = Session(engine)
                session.add(wheelSystem)
                session.commit()
                session.close()
                print("Wheel system added!")
                break
            else:
                break

    nav_up()

# Edit the depreciation relation, or add one if it doesn't exist
def edit_depreciation(vin):
    nav_down("edit_depreciation")

    session = Session(engine, future=True)
    statement = db.select(DepreciationFactors).where(DepreciationFactors.vin == vin)
    result = session.execute(statement).first()
    session.close()

    depreciationFactors = None

    if result:
        depreciationFactors = result.DepreciationFactors

    while True:
        if depreciationFactors:
            options = ["Frame Damage", "Accidents", "Salvage", "View Wheel System", "Save & Go Back"]
            selection = get_input(options)
            if selection > 0 and selection < len(options) - 1:
                if selection == 1:
                    value = ynput("Is the frame damaged (y/n): ")
                    depreciationFactors.frameDamaged = format_for_db(value, "boolean")
                elif selection == 2:
                    value = ynput("Has the vehicle been in any accidents (y/n): ")
                    depreciationFactors.hasAccidents = format_for_db(value, "string", 3)
                else:
                    value = ynput("Is this vehicle salvage (y/n): ")
                    depreciationFactors.salvage = format_for_db(value, "float", 4, 1)
            elif selection == len(options) - 1:
                print_listing("wheel", arg_object=depreciationFactors)
            elif selection == len(options):
                session = Session(engine)
                session.query(DepreciationFactors).filter(DepreciationFactors.vin == vin).update({
                    "frameDamaged": depreciationFactors.frameDamaged,
                    "hasAccidents": depreciationFactors.hasAccidents,
                    "salvage": depreciationFactors.salvage
                })
                session.commit()
                session.close()
                print("")
                print("Depreciation factors saved.")
                break
            elif selection == 0:
                break
            else:
                sys.exit()
        else:
            new_interior = ynput("Depreciation factors not found. Would you like to add them (y/n)?: ")
            if new_interior:
                print("")
                frameDamaged = ynput("Is the vehicle's frame damaged (y/n): ")
                hasAccidents = ynput("Has this vehicle been involved in any accidents (y/n): ")
                salvage = ynput("Is this vehicle salvage (y/n): ")
                depreciationFactors = DepreciationFactors(
                    vin=format_for_db(vin, "string", 17),
                    frameDamaged=format_for_db(frameDamaged, "boolean"),
                    hasAccidents=format_for_db(hasAccidents, "boolean"),
                    salvage=format_for_db(salvage, "boolean")
                )
                session = Session(engine)
                session.add(depreciationFactors)
                session.commit()
                session.close()
                print("Depreciation factors added!")
                break
            else:
                break

    nav_up()

# Deactivate a filter (doesn't actually remove it,
# just sets its active property to False)
def removefilters():
    nav_down("remove_filters")
    print("Select a filter to deactivate it")
    while True:
        active_filters = filter(active_filter, g_filters)
        options = []
        option_names = []
        for f in active_filters:
            option_names.append(f["name"])
            options.append(f["name"] + " " + f["relationship"] + " " + str(f["value"]))

        if len(options) == 0:
            print("No active filters; returning to search.")
            nav_up()
            return

        selection = get_input(options)
        if selection > 0 and selection <= len(options):
            for f in g_filters:
                if (f["name"] == option_names[selection - 1]):
                    f["active"] = 0
                    break
        elif selection == 0:
            break
        elif selection == -1:
            sys.exit()

    nav_up()

# Edit or add a filter - same view for both,
# breaking it down similar to Listings is
# inefficient
def editfilter(index):
    nav_down("edit_filter")
    f = g_filters[index]
    prompt1 = "Enter one of "
    prompt2 = "Select a value for this filter: "
    if (f["f_type"] == "range"):
        prompt1 += "'>', '>=', '=', '!=', '<', '<='"
    elif f['f_type'] == 'equality':
        prompt1 += "'=', '!='"
    else:
        prompt2 = "Select a value for this filter (1/0 for true/false): "
    
    prompt1 += " for the " + f["name"] + " filter operator: "

    if f['f_type'] != 'boolean':
        rel = input(prompt1)
    else:
        rel = '='
    val = input(prompt2)

    f["active"] = 1
    f["relationship"] = rel
    f["value"] = val

    if f["f_type"] == "boolean":
        f["value"] = True if val == "1" else False

    nav_up()

# Add filters (redirects to edit filter after selection)
def addfilters():
    nav_down("add_filters")
    options = []
    for f in g_filters:
        options.append(f["name"])
    while True:
        selection = get_input(options)
        if (selection > 0 and selection <= len(g_filters)):
            editfilter(selection - 1)
        elif (selection == 0):
            nav_up()
            break
        elif (selection == -1):
            sys.exit()

# choose what kind of sorting should be active (only one at a time)
def selectsort():
    nav_down("select_sort")

    print("")
    current = "None"
    currentIndex = -1
    options = []

    for i, sort in enumerate(g_sorting):
        if (sort["active"]):
            current = sort["name"] + " [" + ("High-Low" if sort["type"] == "inverted" else "Low-High") + "]"
            currentIndex = i
        options.append(sort["name"] + " [" + ("High-Low" if sort["type"] == "inverted" else "Low-High") + "]")
    
    while True:
        print("")
        print("Active sort: " + current)
        selection = get_input(options)
        if (selection > 0 and selection <= len(options)):
            if currentIndex == selection - 1:
                g_sorting[selection - 1]["active"] = False
                currentIndex = -1
                current = "None"
            else:
                if (currentIndex > -1):
                    g_sorting[currentIndex]["active"] = False
                g_sorting[selection - 1]["active"] = True
                currentIndex = selection - 1
                current = g_sorting[selection - 1]["name"] + " [" + ("High-Low" if g_sorting[selection - 1]["type"] == "inverted" else "Low-High") + "]"
        elif selection == 0:
            break
        elif selection == -1:
            sys.exit()

    nav_up()

def days_to_class(x):
        '''
        if x < 6:  #very fast
             return 0
        elif x >= 6 and x < 35:  #fast
             return 1
        elif x >= 35 and x < 77:  #average
             return 2
        elif x >= 100 and x < 154:  #slow
             return 3
        elif x >= 154:  #very slow
             return 4
        

        if x < 14:  #very fast
             return 0
        elif x >= 14 and x < 90:  #fast
             return 1
        elif x >= 90:  #average
             return 2
        
        '''
        if x < 77:  #very fast
             return 0
        elif x >= 77:  #fast
             return 1
        

# Start Datamining
def dataMine():
    
    Car_data = pd.read_sql_query('select bodyType,height,width,length,color,year,franchiseMake from Car',connection)
    Interior_data = pd.read_sql_query('select backLegroom,frontLegroom,interiorColor,maximumSeating from Interior',connection)
    Wheel_system_data = pd.read_sql_query('select wheelSystem,wheelbase from WheelSystem',connection)
    Engine_data = pd.read_sql_query('select engineType,engineDisplacement,horsepower,transmission from Engine',connection)
    Fuel_specs_data = pd.read_sql_query('select fuelTankVolume,fuelType from FuelSpecs',connection)
    Trim_package_data = pd.read_sql_query('select trimName from TrimPackage',connection)
    Listing_data = pd.read_sql_query('select daysOnMarket,price from Listing',connection)
    Dealer_data = pd.read_sql_query('select franchiseDealer from DealerDetails',connection)

    Car_data = Car_data.join(Interior_data)
    Car_data = Car_data.join(Wheel_system_data)
    Car_data = Car_data.join(Engine_data)
    Car_data = Car_data.join(Fuel_specs_data)
    Car_data = Car_data.join(Trim_package_data)
    Car_data = Car_data.join(Listing_data)
    Car_data = Car_data.join(Dealer_data)
    nodes = Car_data

    #print(nodes)
    
    LabelEncoderObject = LabelEncoder()
    nodes['encoded_wheel_system'] = LabelEncoderObject.fit_transform(nodes['wheelSystem'].astype(str))
    nodes['encoded_transmission'] = LabelEncoderObject.fit_transform(nodes['transmission'].astype(str))
    nodes['encoded_franchise_make'] = LabelEncoderObject.fit_transform(nodes['franchiseMake'].astype(str))
    nodes['encoded_fuel_type'] = LabelEncoderObject.fit_transform(nodes['fuelType'].astype(str))
    nodes['encoded_engine_type'] = LabelEncoderObject.fit_transform(nodes['engineType'].astype(str))
    nodes['encoded_body_type'] = LabelEncoderObject.fit_transform(nodes['bodyType'].astype(str))
    nodes['encoded_franchise_dealer'] = LabelEncoderObject.fit_transform(nodes['franchiseDealer'].astype(str))
    nodes['encoded_trim_name'] = LabelEncoderObject.fit_transform(nodes['trimName'].astype(str))
    nodes['encoded_exterior_color'] = LabelEncoderObject.fit_transform(nodes['color'].astype(str))
    nodes['encoded_interior_color'] = LabelEncoderObject.fit_transform(nodes['interiorColor'].astype(str))

    #keep only the numerical verison
    encoded_nodes = nodes.drop(['wheelSystem','transmission','franchiseMake','fuelType','engineType','bodyType','franchiseDealer','trimName','color','interiorColor'],axis='columns')

    #seperate days on market into its own series
    leafs = encoded_nodes['daysOnMarket']
    encoded_nodes = encoded_nodes.drop('daysOnMarket', axis='columns')

     #sort through the days on market into 5 categories
    print('Starting apply function')
    leafCat = leafs.apply(days_to_class)

    #join days on market back into encoded so we can clean out any rows that have nulls so it dosen't affect the decision tree
    encoded_nodes = encoded_nodes.join(leafCat)
    encoded_nodes = encoded_nodes.dropna()

    #print(encoded_nodes)

    #seperate the clean set into the leafs and potential nodes
    leafs_full = encoded_nodes['daysOnMarket']
    nodes_full = encoded_nodes.drop('daysOnMarket', axis='columns')

    #split into test and training sets for the decision trees
    node_train,node_test,leaf_train,leaf_test = train_test_split(nodes_full,leafs_full,test_size=0.2,train_size=0.8,random_state=81)

    print('split the thing')

    #build the decision tree with the train sets
    classifier = tree.DecisionTreeClassifier(max_depth=6,random_state=0)
    classifier = classifier.fit(node_train, leaf_train)

    print('fitted')

    #make predictions on test set
    leaf_predicted = classifier.predict(node_test)

    print('predict test set')

    #measure the accuracy
    print(accuracy_score(leaf_test,leaf_predicted)*100)

    print('accuracy tested')

    print('graphing - might take a while')

    try:
        list_of_class_names = ["sells fast","sells slow"]
        dot_data = tree.export_graphviz(classifier, out_file=None,feature_names=node_train.columns,class_names=list_of_class_names,filled=True) 
        graph = graphviz.Source(dot_data) 
        graph.render("DaysOnMarketGraph") 
    except:
        print("an error occured, try seeing if you installed graphviz properly")
        print("you will need to install graphiz both on pip AND on its own")

    print("categories used for decision tree")
    print(node_train.columns)

startup()