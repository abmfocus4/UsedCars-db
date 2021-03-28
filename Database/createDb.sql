-- Clean dB
drop table if exists User;
drop table if exists PhoneNumber;
drop table if exists Listing;
drop table if exists Address1;
drop table if exists Address2;
drop table if exists DealerDetails;
drop table if exists Appointment;
drop table if exists Car;
drop table if exists TrimPackage;
drop table if exists Interior;
drop table if exists WheelSystem;
drop table if exists Engine;
drop table if exists FuelSpecs;
drop table if exists DepreciationFactors;
drop table if exists CarOwners;
-- Clean outfile
\! rm -f cars-outfile.txt
tee cars-outfile.txt;
warnings;
-- User
select 'User' as '';
create table User (
    email varchar(125),
    firstName varchar(125),
    lastName varchar(125),
    pass varchar(40) not null,
    userType varchar(8) not null,
    primary key (email),
    check(email regexp '^\S+@\S+\.\S+$'),
    check(
        pass regexp '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    ),
    check(userType in ('Admin', 'Customer', 'Dealer'))
);
insert into User(email, firstName, lastName, pass, userType)
values (
        `bmalapat@uwaterloo.ca`,
        `Meg`,
        `Alapati`,
        `password`,
        `Admin`
    ),
    (
        `s2ishraq@uwaterloo.ca`,
        `Shwapneel`,
        `Ishraq`,
        `password`,
        `Admin`
    ),
,
    (
        `connor.peter.barker@uwaterloo.ca`,
        `Connor`,
        `Barker`,
        `password`,
        `Admin`
    );
-- PhoneNumber
select 'PhoneNumber' as '';
create table PhoneNumber (
    userEmail varchar(125),
    phoneNumber decimal(15, 0),
    primary key(userEmail, phoneNumber),
    foreign key (userEmail) references User(email)
);
-- Listing
select 'Listing' as '';
create table Listing (
    listingId int not null unique,
    listingDate date not null,
    daysOnMarket int,
    description varchar(400),
    mainPictureURL varchar(400),
    majorOptions varchar(400),
    price decimal(9, 2),
    dealerEmail varchar(125),
    primary key (listingId)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table Listing fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set listingId = @col39,
    listingDate = @col37,
    daysOnMarket = @col11,
    description = @col13,
    mainPictureURL = @col41,
    majorOptions = @col42,
    price = @col49;
-- Address1
select 'Address1' as '';
create table Address1 (
    listingId int not null unique,
    zip varchar(32),
    city varchar(125),
    primary key (listingId),
    foreign key (listingId) references Listing(listingId)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table Address1 fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set listingId = @col39,
    zip = @col12,
    city = @col8;
-- Address2
select 'Address2' as '';
create table Address2 (
    listingId int not null unique,
    latitude decimal(2, 2),
    longitude decimal(3, 2),
    primary key (listingId),
    foreign key (listingId) references Listing(listingId)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table Address2 fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set listingId = @col39,
    latitude = @col35,
    longitude = @col40;
-- DealerDetails
select 'DealerDetails' as '';
create table DealerDetails (
    listingId decimal(9, 0),
    franchiseDealer decimal(2, 2),
    sellerRating decimal(3, 2),
    primary key (listingId),
    foreign key (listingId) references Listing(listingId)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table DealerDetails fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set listingId = @col39,
    franchiseDealer = @col20,
    sellerRating = @col52;
-- Appointment
select 'Appointment' as '';
create table Appointment (
    appointmentNumber int not null,
    dealerEmail not null,
    customerEmail not null,
    appointmentDateTime not null datetime,
    information varchar(400),
    primary key (appointmentNumber, dealerEmail, customerEmail),
    foreign key (dealerEmail) references User(email),
    foreign key (customerEmail) references User(email)
);
-- Car
select 'Car' as '';
create table Car (
    VIN varchar(17),
    bodyType varchar(40),
    height decimal(4, 1),
    year YEAR,
    modelName varchar(40),
    franchiseMake varchar(40),
    isFleet varchar(5) check(isFleet in ('False', 'True', null)),
    isCab varchar(5) check(isCab in ('False', 'True', null)),
    isNew varchar(5) check(isNew in ('False', 'True', null)),
    listingId int not null unique,
    foreign key (listingId) references Listing(listingId),
    primary key (VIN)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table Car fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set VIN = @col1,
    bodyType = @col6,
    height = left(@col26, char_length(@col26) -2),
    year = @col66,
    modelName = @col46,
    franchiseMake = @col21,
    isFleet = nullif(@col18, ''),
    isCab = nullif(@col30, ''),
    isNew = nullif(@col33, ''),
    listingId = @col39;
-- DepreciationFactors
select 'DepreciationFactors' as '';
create table DepreciationFactors (
    VIN varchar(17) not null,
    frameDamaged char(5) check(frameDamaged in ('False', 'True', null)),
    hasAccidents char(5) check(hasAccidents in ('False', 'True', null)),
    salvage char(5) check(salvage in ('False', 'True', null)),
    savingsAmount decimal(7, 2),
    primary key (VIN),
    foreign key (VIN) references Car(VIN)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table DepreciationFactors fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set frameDamaged = @col19,
    hasAccidents = @col25,
    salvage = @col50,
    VIN = @col1,
    savingsAmount = @col51;
-- WheelSystem
select 'WheelSystem' as '';
create table WheelSystem (
    VIN varchar(17) not null,
    wheelSystem char(3),
    wheelSystemDisplay varchar(40),
    wheelbase decimal(4, 1),
    primary key (VIN),
    foreign key (VIN) references Car(VIN)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table WheelSystem fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set wheelbase = nullif(left(@col64, char_length(@col64) -2), ''),
    wheelSystem = @col62,
    VIN = @col1,
    wheelSystemDisplay = @col63;
-- Engine
select 'Engine' as '';
create table Engine (
    VIN varchar(17) not null,
    engineCylinders varchar(40),
    engineDisplacement decimal(8, 3),
    engineType varchar(40),
    horsepower decimal(5, 2),
    transmission varchar(40),
    transmissionDisplay varchar(125),
    power varchar(125),
    primary key (VIN),
    foreign key (VIN) references Car(VIN)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table Engine fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set engineCylinders = @col14,
    engineDisplacement = nullif(@col15, ''),
    engineType = @col16,
    horsepower = nullif(@col28, ''),
    transmission = @col57,
    VIN = @col1,
    transmissionDisplay = @col58,
    power = nullif(@col48, '');
-- FuelSpecs
select 'FuelSpecs' as '';
create table FuelSpecs (
    VIN varchar(17) not null,
    fuelTankVolume decimal(4, 1),
    fuelType varchar(40),
    highwayFuelEconomy decimal(5, 2),
    cityFuelEconomy decimal(5, 2),
    primary key (VIN),
    foreign key (VIN) references Car(VIN)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table FuelSpecs fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set fuelTankVolume = left(
        @col23,
        char_length(@col23) -3
    ),
    fuelType = @col24,
    VIN = @col1,
    highwayFuelEconomy = @col27,
    cityFuelEconomy = @col9;
-- Interior
select 'Interior' as '';
create table Interior (
    VIN varchar(17) not null,
    backLegroom decimal(4, 1),
    frontLegroom decimal(4, 1),
    interiorColor varchar(125),
    maximumSeating int,
    primary key (VIN),
    foreign key (VIN) references Car(VIN)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table Interior fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set backLegroom = nullif(left(@col2, char_length(@col2) -2), ''),
    frontLegroom = nullif(left(@col22, char_length(@col22) -2), ''),
    interiorColor = @col29,
    VIN = @col1,
    maximumSeating = nullif(left(@col44, char_length(@col44) -5), '');
-- Trim Package
select 'TrimPackage' as '';
create table TrimPackage (
    VIN varchar(17) not null,
    trimId decimal(5, 0),
    trimName varchar(125),
    primary key (VIN),
    foreign key (VIN) references Car(VIN)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table TrimPackage fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set trimId = nullif(@col59, ''),
    trimId = trim(
        leading 't'
        from @col59
    ),
    VIN = @col1,
    trimName = @col60;
-- CarOwners
select 'CarOwners' as '';
create table CarOwners (
    VIN varchar(17) not null,
    ownercount int,
    primary key (VIN),
    foreign key (VIN) references Car(VIN)
);
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table CarOwners fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @col1,
    @col2,
    @col3,
    @col4,
    @col5,
    @col6,
    @col7,
    @col8,
    @col9,
    @col10,
    @col11,
    @col12,
    @col13,
    @col14,
    @col15,
    @col16,
    @col17,
    @col18,
    @col19,
    @col20,
    @col21,
    @col22,
    @col23,
    @col24,
    @col25,
    @col26,
    @col27,
    @col28,
    @col29,
    @col30,
    @col31,
    @col32,
    @col33,
    @col34,
    @col35,
    @col36,
    @col37,
    @col38,
    @col39,
    @col40,
    @col41,
    @col42,
    @col43,
    @col44,
    @col45,
    @col46,
    @col47,
    @col48,
    @col49,
    @col50,
    @col51,
    @col52,
    @col53,
    @col54,
    @col55,
    @col56,
    @col57,
    @col58,
    @col59,
    @col60,
    @col61,
    @col62,
    @col63,
    @col64,
    @col65,
    @col66
)
set VIN = @col1,
    ownercount = nullif(@col47, '');
create temporary table dumpingGround like CarOwners;
insert into dumpingGround (
        select distinct *
        from CarOwners
        where ownercount is not null
    );
truncate CarOwners;
insert into CarOwners (
        select *
        from dumpingGround
    );
drop temporary table if exists dumpingGround;
-- Done
notee