drop table if exists TrimPackage;
drop table if exists Interior;
drop table if exists WheelSystem;
drop table if exists Engine;
drop table if exists FuelSpecs;
drop table if exists DepreciationFactors;
drop table if exists User;
drop table if exists PhoneNumber;
drop table if exists Address1;
drop table if exists Address2;
\! rm -f cars-outfile.txt
tee cars-outfile.txt;
warnings;
-- Trim Package
select 'TrimPackage' as '';
create table TrimPackage (trimId decimal(5, 0), trimName varchar(125));
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
set trimId = if (@col59 like '', NULL, @col59),
    trimId = trim(
        leading 't'
        from @col59
    ),
    trimName = @col60;
create temporary table dumpingGround like TrimPackage;
insert into dumpingGround (
        select distinct *
        from TrimPackage
        where trimId is not null
            and trimName is not null
    );
truncate TrimPackage;
insert into TrimPackage (
        select *
        from dumpingGround
    );
drop temporary table if exists dumpingGround;
alter table TrimPackage
add unique (trimId, trimName);
alter table TrimPackage
add packageId int not null auto_increment primary key first;
-- Interior
select 'Interior' as '';
create table Interior (
    backLegroom decimal(4, 1),
    frontLegroom decimal(4, 1),
    interiorColor varchar(125),
    maximumSeating int
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
set backLegroom = left(@col2, char_length(@col2) -2),
    frontLegroom = left(@col22, char_length(@col22) -2),
    interiorColor = @col29,
    maximumSeating = left(@col44, char_length(@col44) -5);
create temporary table dumpingGround like Interior;
insert into dumpingGround (
        select distinct *
        from Interior
    );
truncate Interior;
insert into Interior (
        select *
        from dumpingGround
    );
drop temporary table if exists dumpingGround;
alter table Interior
add unique (
        backLegroom,
        frontLegroom,
        interiorColor,
        maximumSeating
    );
alter table TrimPackage
add packageId int not null auto_increment primary key first;
-- WheelSystem
select 'WheelSystem' as '';
create table WheelSystem (
    -- TODO: confirm it's 3
    wheelSystem char(3),
    wheelSystemDisplay varchar(40),
    wheelbase decimal(4, 1)
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
set wheelbase = left(@col64, char_length(@col64) -2),
    wheelSystem = @col62,
    wheelSystemDisplay = @col63;
create temporary table dumpingGround like WheelSystem;
insert into dumpingGround (
        select distinct *
        from WheelSystem
    );
truncate WheelSystem;
insert into WheelSystem (
        select *
        from dumpingGround
    );
drop temporary table if exists dumpingGround;
alter table WheelSystem
add unique (
        wheelSystem,
        wheelSystemDisplay,
        wheelbase
    );
alter table WheelSystem
add systemId int not null auto_increment primary key first;
-- Engine
select 'Engine' as '';
create table Engine (
    engineCylinders varchar(40),
    engineDisplacement decimal(6, 2),
    engineType varchar(40),
    horsepower decimal(5, 2),
    transmission varchar(40),
    transmissionDisplay varchar(125)
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
    engineDisplacement = @col15,
    engineType = @col16,
    horsepower = @col28,
    transmission = @col57,
    transmissionDisplay = @col58;
create temporary table dumpingGround like Engine;
insert into dumpingGround (
        select distinct *
        from Engine
    );
truncate Engine;
insert into Engine (
        select *
        from dumpingGround
    );
drop temporary table if exists dumpingGround;
alter table Engine
add unique (
        engineDisplacement,
        engineType,
        horsepower,
        transmission,
        transmissionDisplay
    );
alter table Engine
add engineId int not null auto_increment primary key first;
-- FuelSpecs
select 'FuelSpecs' as '';
create table FuelSpecs (
    fuelTankVolume decimal(4, 1),
    fuelType varchar(40),
    highwayFuelEconomy decimal(5, 2),
    cityFuelEconomy decimal(5, 2)
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
    highwayFuelEconomy = @col27,
    cityFuelEconomy = @col9;
create temporary table dumpingGround like FuelSpecs;
insert into dumpingGround (
        select distinct *
        from FuelSpecs
    );
truncate FuelSpecs;
insert into FuelSpecs (
        select *
        from dumpingGround
    );
drop temporary table if exists dumpingGround;
alter table FuelSpecs
add unique (
        fuelTankVolume,
        fuelType,
        highwayFuelEconomy,
        cityFuelEconomy
    );
alter table FuelSpecs
add specId int not null auto_increment primary key first;
-- DepreciationFactors
select 'DepreciationFactors' as '';
create table DepreciationFactors (
    frameDamaged char(5) check(frameDamaged in ('False', 'True', null)),
    hasAccidents char(5) check(hasAccidents in ('False', 'True', null)),
    salvage char(5) check(salvage in ('False', 'True', null)),
    savingsAmount decimal(7, 2)
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
    savingsAmount = @col51;
create temporary table dumpingGround like DepreciationFactors;
insert into dumpingGround (
        select distinct *
        from DepreciationFactors
    );
truncate DepreciationFactors;
insert into DepreciationFactors (
        select *
        from dumpingGround
    );
drop temporary table if exists dumpingGround;
alter table DepreciationFactors
add unique (
        frameDamaged,
        hasAccidents,
        salvage,
        savingsAmount
    );
alter table DepreciationFactors
add factorId int not null auto_increment primary key first;
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
-- Address1
select 'Address1' as '';
create table Address1 (
    userEmail varchar(125),
    zip varchar(32),
    primary key(userEmail),
    foreign key (userEmail) references User(email)
);
-- Address2
select 'Address2' as '';
create table Address2 (
    userEmail varchar(125),
    latitude decimal(2, 2),
    longitude decimal(3, 2),
    primary key(userEmail),
    foreign key (userEmail) references User(email)
);
notee