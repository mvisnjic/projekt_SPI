# POLICE STATION SK
SELECT dp.police_station_sk, c.id
FROM crimes.crime c,
	 crimes.offense o,
     crimes.location l,
     crimes.police_station p,
     crimes.district d
INNER JOIN crimes_dimenzije.dim_police_station dp
ON dp.district = d.name
WHERE c.offense_fk = o.id
AND  c.location_fk = l.id
AND  c.police_station_fk = p.id
AND  d.id = p.district_fk;

# SHOOTING SK
SELECT sho.shooting_sk, c.id
FROM crimes.crime c
INNER JOIN crimes_dimenzije.dim_shooting sho
ON c.shooting = sho.shooting
where sho.shooting IS NOT NULL;


# LOCATION_SK 
SELECT dl.location_sk, l.id
FROM  crimes.location l,
	  crimes.street s,
      crimes_dimenzije.dim_location dl
WHERE l.street_fk = s.id
AND dl.street_name = s.name
ORDER BY l.id;

# OFFENSE SK
SELECT dimof.offense_sk, o.id
FROM  crimes.offense o,
	  crimes.ucr_part uc,
      crimes_dimenzije.dim_offense dimof
WHERE o.ucr_part_fk = uc.id
AND dimof.ucr_part = uc.name
AND dimof.code_group = o.code_group;

# TIME SK + crime_description -- ispisuje 319030 podataka a trebalo bi 319073, ne znam kako to riješiti.. problem je sigurno kod dimenzije time, negdje se izgubilo 43 podatka..
SELECT c.crime_description, dimt.time_sk, c.id
FROM crimes.crime c,
	 crimes_dimenzije.dim_time dimt
WHERE c.occured_on_date = dimt.occured_on_date
AND c.day_of_week = dimt.day_of_week
AND c.year = dimt.YEAR
ORDER BY c.id;

