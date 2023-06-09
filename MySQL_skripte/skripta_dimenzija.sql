DROP DATABASE crimes_dimenzije;
CREATE DATABASE crimes_dimenzije;
USE crimes_dimenzije;

CREATE TABLE dim_crime (
	crime_sk INTEGER PRIMARY KEY AUTO_INCREMENT,
	id INTEGER,
    crime_description MEDIUMTEXT,
    dim_location_sk INTEGER,
    dim_offense_sk INTEGER,
    dim_time_sk INTEGER,
    dim_police_station_sk INTEGER,
    dim_shooting_sk INTEGER,
    CONSTRAINT dim_location_id FOREIGN KEY (dim_location_sk) REFERENCES crimes_dimenzije.dim_location(location_sk),
    CONSTRAINT dim_offense_id FOREIGN KEY (dim_offense_sk) REFERENCES crimes_dimenzije.dim_offense(offense_sk),
    CONSTRAINT dim_time_id FOREIGN KEY (dim_time_sk) REFERENCES crimes_dimenzije.dim_time(time_sk),
    CONSTRAINT dim_police_station_id FOREIGN KEY (dim_police_station_sk) REFERENCES crimes_dimenzije.dim_police_station(police_station_sk),
    CONSTRAINT dim_shooting_id FOREIGN KEY (dim_shooting_sk) REFERENCES crimes_dimenzije.dim_shooting(shooting_sk)
);



CREATE TABLE dim_time (
	time_sk INTEGER PRIMARY KEY,
    id INTEGER,
    day_of_week VARCHAR(45),
    hour TINYINT,
    month TINYINT,
    YEAR INTEGER,
    occured_on_date DATETIME
);

CREATE TABLE dim_police_station (
	police_station_sk INTEGER PRIMARY KEY,
    id INTEGER,
    address VARCHAR(150),
    district VARCHAR(20),
    version INT,
    date_from DATETIME,
    date_to DATETIME
);

CREATE TABLE dim_shooting (
	shooting_sk INTEGER PRIMARY KEY,
    id INTEGER,
	shooting VARCHAR(10),
    version INT,
    date_from DATETIME,
    date_to DATETIME
);

CREATE TABLE dim_offense (
	offense_sk INTEGER PRIMARY KEY,
    id INTEGER,
    ucr_part VARCHAR(45),
    code_group VARCHAR(45),
	version INT,
    date_from DATETIME,
    date_to DATETIME
);

CREATE TABLE dim_location(
	location_sk INTEGER PRIMARY KEY,
    id INTEGER,
    coordinates VARCHAR(100),
    street_name VARCHAR(100),
    version INT,
    date_from DATETIME,
    date_to DATETIME
);


# NAKON ŠTO SMO UBACILI PODATKE IZ PENTAHA, MORAMO SAMO IZMJENITI ID 31-INVESTIGATE PERSON, I STAVITI MU UCR_PART- PART THREE. MOŽE SE I OBRISATI ALI OVAKO JE BOLJE..
UPDATE crimes_dimenzije.dim_offense
SET ucr_part = 'Part Three'
where id = 31;

# ZBOG KRIVIH NEKIH PODATAKA MORAMO ISTO PREIMENOVATI UCR PART NAME IZ N, U PART THREE
UPDATE crimes.ucr_part uc
INNER JOIN crimes.crime c ON c.id=uc.id
SET uc.name = 'Part Three'
WHERE uc.name = 'N'
AND c.crime_description = 'INVESTIGATE PERSON';