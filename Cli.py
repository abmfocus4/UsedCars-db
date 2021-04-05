import re
import sys
import json
import datetime
import sqlalchemy as db
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
# this script also requires pymysql & cryptography to be installed with the below command
# `pip3 install pymysql cryptography`

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    email = db.Column('email', db.String(125), primary_key=True, nullable=False)
    firstName = db.Column('firstName', db.String(125), nullable=True)
    lastName = db.Column('lastName', db.String(125), nullable=True)
    password = db.Column('pass', db.String(40), nullable=False)
    userType = db.Column('userType', db.String(8), nullable=False)

    def __repr__(self):
        return "<User(email='%s', firstName='%s', lastName='%s', pass='%s', userType='%s')>" % (
                             self.email, self.firstName, self.lastName, self.password, self.userType)

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

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3307,
    'user': 'admin',
    'password': 'password',
    'database': 'Cars'
}

g_user = None
g_loc = []
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
    return

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

def parse(string):
    try:
        #check if string is a number for menu
        int(string)
        return int(string)
    except ValueError:
        return 0 if string == "b" else -1

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

def get_input(options):
    list_options(options)
    if len(options) == 0:
        print("No options available; enter 'b' to return to the previous screen.")
    selection = parse(input("Select an option: "))
    while (selection < -1 or selection > len(options) and len(options) > 0):
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
    options = ["Search Listings"]

    if (g_user.userType != "Customer"):
        options.extend(["Create Listing", "View Your Listings"])

    nav_down("main")
    while (1):
        selection = get_input(options)
        if (selection == 1):
            search()
        elif (selection == 2):
            new_listing()
        elif (selection == 3):
            owned_listings()
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
    global g_user
    options = ["Sign Up", "Log In"]
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
                g_phone = input("Enter your phone number (leave blank if n/a): ")
                if ( ( g_phone.isnumeric() and len(g_phone)<=15 ) or ( len(g_phone) == 0 ) ):
                   is_valid_phone = True

            is_valid_postal = False
            while ( not is_valid_postal ):
                g_postal = input("Enter your postal code (leave blank if n/a): ")
                if ( ( len(g_postal)<=32 ) or ( g_postal == "no" ) ):
                   is_valid_postal = True       

            g_user = User(email=g_email, firstName=g_firstname, lastName=g_lastname, password=g_password, userType=userType)

            session = Session(engine)
            session.add(g_user)
            session.commit()

            break
        elif (selection == 2):
            bad_info_repeat = True

            while(bad_info_repeat):
                f_email = input("email: ")
                f_password = input("password: ")

                error_because_of_bad_password = 0

                session = Session(engine, future=True)
                statement = db.select(User).where(User.email == str(f_email))
                results = session.execute(statement).all()
                session.close()

                if (len(results) == 1):
                    if (f_password != results[0].User.password):
                        print("Incorrect password.")
                        error_because_of_bad_password = 1
                        continue
                    else:
                        g_user = results[0].User
                        bad_info_repeat = False
                    
                if (error_because_of_bad_password == 0):
                   print("user not found")
                   continue
            break
            
        elif (selection == 0):
            continue
        elif (selection == -1):
            continue
    
    print("Login successful! Welcome to Ottotradr,", g_user.firstName)

    nav_up()

def owned_listings():
    nav_down("owned_listings")

    print("")
    sys.stdout.write("\rRetrieving owned listings (this may take some time)...")

    session = Session(engine, future=True)
    statement = db.select(Car, Listing).join(Listing).where(Listing.dealerEmail == str(g_user.email))
    results = session.execute(statement).all()

    if (len(results) == 0):
        sys.stdout.write("\rLooks like you don't have any listings! You can create them from the main page.")
        sys.stdout.flush()
    else:
        while (1):
            sys.stdout.write("\rYou can see your listings below; select one to view it in more detail, edit, or remove it.")
            print("")
            options = []
            option_ids = []
            for car, listing in results:
                option_ids.append(car.listingId)
                options.append(car.franchiseMake + " " + car.modelName + " [$" + str(listing.price) + "]")
            selection = get_input(options)
            if (selection > 0 and selection <= len(options)):
                detail(option_ids[selection - 1])
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
    is_valid_vin = False
    vin = 0

    while True:
        vin = input("Enter vehicle VIN number: ")
        if ( vin.isnumeric() and len(vin) >= 11 and len(vin) <= 17 ):
            break
    
    make = input("Enter vehicle make: ")
    model = input("Enter vehicle model: ")
    height = input("Enter vehicle height: ")
    bodyType = input("Enter vehicle body type: ")
    year = input("Enter vehicle year of make: ")
    price = input("Enter desired list price: ")
    isNew = ynput("Is this vehicle new (y/n): ")
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
    
    if not isNew:
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
    print("New: " + ("True" if isNew else "False"))
    print("Cab: " + ("True" if isCab else "False"))
    if trimPackage is not None:
        print("Trim package: " + str(trimPackage.trimName))
    if hasEngine:
        print("Engine displacement: " + str(carEngine.engineDisplacement) + "mL")
        print("Engine type: " + str(carEngine.engineType))
        print("Engine cylinders: " + str(carEngine.engineCylinders))
        print("Transmission: " + str(carEngine.transmission))
        print("Horsepower: " + str(carEngine.horsepower) + "bhp")
    if hasInterior:
        print("Front legroom: " + str(interior.frontLegroom) + "cm")
        print("Rear legroom: " + str(interior.backLegroom) + "cm")
        print("Interior colour: " + str(interior.interiorColor))
        print("Maximum seating: " + str(interior.maximumSeating))
    if hasFuel:
        print("Fuel tank volume: " + str(fuelSpecs.fuelTankVolume) + "L")
        print("Fuel type: " + str(fuelSpecs.fuelType))
        print("City economy: " + str(fuelSpecs.cityFuelEconomy) + "kpL")
        print("Highway economy: " + str(fuelSpecs.highwayFuelEconomy) + "kpL")
    if hasWheelbase:
        print("Drive system: " + str(wheelSystem.wheelSystem))
        print("Wheelbase: " + str(wheelSystem.wheelbase) + "cm")
    if not isNew:
        print("Damaged frame: " + str(depreciationFactors.frameDamaged))
        print("Has been in an accident: " + str(depreciationFactors.hasAccidents))
        print("Is salvage: " + str(depreciationFactors.salvage))

    print("")

    listingDescription = input("Enter a description for this listing: ")

    listing = Listing(
        listingDate=datetime.date.today(),
        daysOnMarket=0,
        description=format_for_db(listingDescription, "string", 1000),
        price=format_for_db(price, "float", 9, 2),
        dealerEmail=format_for_db(g_user.email, "string", 125)
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
            year=format_for_db(year, "integer"),
            modelName=format_for_db(model, "string", 40),
            franchiseMake=format_for_db(make, "string", 40),
            isNew=format_for_db(isNew, "boolean"),
            isCab=format_for_db(isCab, "boolean"),
            listingId=format_for_db(listing.listingId, "integer")
        )

        session = Session(engine)
        session.add(car)
        session.commit()

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
    owned = False

    print("")
    print("Make: " + result.Car.franchiseMake)
    print("Model: " + result.Car.modelName)
    print("Year: " + str(result.Car.year))
    print("Price: " + str(result.Listing.price))
    print("New: " + result.Car.isNew)
    print("VIN: " + result.Car.vin)
    options = []

    while (1):
        if (g_user.userType == "Dealer"):
            if result.Listing.dealerEmail == g_user.email:
                options = ["Edit Listing", "Remove Listing"]
                owned = True
        elif (g_user.userType == "Customer"):
            options = ["Purchase Vehicle"]
        else:
            options = ["Purchase Vehicle", "Edit Listing", "Remove Listing"]
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
                # do something to buy the vehicle
                
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