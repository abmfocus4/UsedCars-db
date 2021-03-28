drop table if exists TrimPackage;
\ ! rm - f cars_outfile.txt tee cars_outfile.txt;
warnings;
-- TODO: manage nulls in PK
-- Trim Package
select 'TrimPackage' as '';
--create table
create table TrimPackage (trimId int, trimName varchar(125));
-- TODO: load csv data
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
set trimId = substring(@col59, 2);
set trimName = @col60;
--clean table
create temporary table dumpingGround like TrimPackage;
insert into dumpingGround (
        select distinct *
        from TrimPackage
    );
truncate TrimPackage;
insert into TrimPackage (
        select *
        from dumpingGround
    );
drop temporary table if exists dumpingGround;
-- add PK
alter table TrimPackage
add unique (trimId, trimName);
alter table TrimPackage
add trimPackageId int not null auto_increment primary key first;

-- Interior
select 'Interior' as '';
--create table
create table Interior (
    backLegroom decimal(3, 1),
    frontLegroom decimal(3, 1),
    interiorColor varchar(125),
    maximumSeating int
);
-- TODO: load csv data
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
) -- remove trailing in
set backLegroom = left(@col2, char_length(@col2) -2),
    -- remove trailing in
    frontLegroom = left(@col22, char_length(@col22) -2),
    interiorColor = @col29,
    -- remove trailing seats
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
    wheelbase decimal(3, 1)
);
-- TODO: load csv
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
) -- remove trailing in
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
    engineDisplacement decimal(4, 2),
    engineType varchar(40),
    horsepower decimal(3, 2),
    transmission varchar(40),
    transmissionDisplay varchar(125)
);
-- TODO: load csv data
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
        -- engine_cyclinders is not included
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
--create table
create table FuelSpecs (
    fuelTankVolume decimal(3, 1),
    fuelType varchar(40),
    highwayFuelEconomy decimal(3, 2),
    cityFuelEconomy decimal(3, 2)
);
-- TODO: load csv data
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
) -- remove trailing gal
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
    frameDamaged char(5),
    hasAccidents char(5),
    salvage 
    savings_amount
);