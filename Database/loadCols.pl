#!/usr/bin/env perl -w
# takes tableName and cols list as input
$tableName = <>;
@colNames = ("vin", "back_legroom", "bed", "bed_height", "bed_length", "body_type", "cabin", "city", "city_fuel_economy", "combine_fuel_economy", "daysonmarket", "dealer_zip", "description", "engine_cylinders", "engine_displacement", "engine_type", "exterior_color", "fleet", "frame_damaged", "franchise_dealer", "franchise_make", "front_legroom", "fuel_tank_volume", "fuel_type", "has_accidents", "height", "highway_fuel_economy", "horsepower", "interior_color", "isCab", "is_certified", "is_cpo", "is_new", "is_oemcpo", "latitude", "length", "listed_date", "listing_color", "listing_id", "longitude", "main_picture_url", "major_options", "make_name", "maximum_seating", "mileage", "model_name", "owner_count", "power", "price", "salvage", "savings_amount", "seller_rating", "sp_id", "sp_name", "theft_title", "torque", "transmission", "transmission_display", "trimId", "trim_name", "vehicle_damage_category", "wheel_system", "wheel_system_display", "wheelbase", "width", "year");  # Whatever the column names are in the table

$fileName = "/var/lib/mysql-files/01-Cars/used_cars_data.csv";

$cols = <>;
# @cols = (4, 8, 9, 53);  # The columns I want from the CSV
# $totalCols = 60;

$terminator = "\n";  # Could be just "\n"

$loadCmd = "load data infile '$fileName' ignore into table $tableName fields terminated by ',' enclosed by '\"' lines terminated by '$terminator' ignore 1 lines (";

$curCol = 1;
while (scalar(@cols) > 0) {
    $nextCol = shift @cols;
    while ($curCol < $nextCol) {
	$loadCmd .= "\@t$curCol, ";
	++$curCol;
    }
    ++$curCol;
    $nextName = shift @colNames;
    $loadCmd .= "$nextName, ";
}
$loadCmd .= "\@andTheRest)";
$setCmd = <>;

print $loadCmd,"\n", $setCmd;
