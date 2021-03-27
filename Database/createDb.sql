drop table if exists TrimPackage;
\ ! rm - f cars_outfile.txt tee cars_outfile.txt;
warnings;
-- TODO: manage nulls in PK
-- Trim Package
select 'TrimPackage' as '';
--create table
create table TrimPackage (
    -- trimPackageId int not null auto_increment,
    trimId int,
    trim_name varchar(125) -- primary key (trimPackageId)
);
-- TODO: load csv data
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table TrimPackage fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (@trimId, trim_name)
set trimId = substring(@trimId, 2);
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
add primary key (trimId);
-- TODO: rename cols
-- Interior
select 'Interior' as '';
--create table
create table Interior (
    packageId int not null auto_increment,
    back_legroom decimal(3, 1),
    front_legroom decimal(3, 1),
    interior_color varchar(125),
    maximum_seating int
);
-- TODO: load csv data
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table Interior fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @back_legroom,
    @front_legroom,
    interior_color,
    @maximum_seating
) -- remove trailing in
set back_legroom = left(@back_legroom, char_length(@back_legroom) -2),
    -- remove trailing in
    front_legroom = left(@front_legroom, char_length(@front_legroom) -2),
    -- remove trailing seats
    maximum_seating = left(@front_legroom, char_length(@front_legroom) -5);
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
add primary key (
        back_legroom,
        front_legroom,
        interior_color,
        maximum_seating
    );
-- TODO: rename cols
-- WheelSystem
select 'WheelSystem' as '';
create table WheelSystem (
    systemId int not null auto_increment,
    -- TODO: confirm it's 3
    wheel_system char(3),
    wheel_system_display varchar(40),
    -- remove 2
    wheelbase decimal(3, 1)
);
-- TODO: load csv
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table WheelSystem fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    wheel_system,
    wheel_system_display,
    @wheelbase
) -- remove trailing in
set wheelbase = left(@wheelbase, char_length(@wheelbase) -2);
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
add primary key (
        wheel_system,
        wheel_system_display,
        wheelbase
    );
-- TODO: rename cols
-- Engine
select 'Engine' as '';
create table Engine (
    engineId int not null auto_increment,
    engine_cylinders varchar(40),
    engine_displacement decimal(4, 2),
    engine_type varchar(40),
    horsepower decimal(3, 2),
    transmission varchar(40),
    transmission_display varchar(125)
);
-- TODO: load csv data
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table Engine fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    engine_cylinders,
    engine_displacement,
    engine_type,
    horsepower,
    transmission,
    transmission_display
);
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
add primary key (
        -- engine_cyclinders is not included
        - - type->cylinders engine_displacement,
        engine_type,
        horsepower,
        transmission,
        transmission_display
    );
-- TODO: rename cols
-- FuelSpecs
select 'FuelSpecs' as '';
--create table
create table FuelSpecs (
    specId int not null auto_increment,
    fuel_tank_volume decimal(3, 1),
    fuel_type varchar(40),
    highway_fuel_economy decimal(3, 2),
    city_fuel_economy decimal(3, 2)
);
-- TODO: load csv data
load data infile '/var/lib/mysql-files/01-Cars/used_cars_data.csv' ignore into table FuelSpecs fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines (
    @fuel_tank_volume,
    fuel_type,
    highway_fuel_economy,
    city_fuel_economy
) -- remove trailing gal
set fuel_tank_volume = left(@fuel_tank_volume, char_length(@fuel_tank_volume) -3);
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
add primary key (
        fuel_tank_volume,
        fuel_type,
        highway_fuel_economy,
        city_fuel_economy
    );
-- TODO: rename cols
-- DepreciationFactors
select 'DepreciationFactors' as '';
create table DepreciationFactors (
    factorId int not null auto_increment,
    frame_damaged char(5),
    has_accidents char(5),
    salvage
    savings_amount
);